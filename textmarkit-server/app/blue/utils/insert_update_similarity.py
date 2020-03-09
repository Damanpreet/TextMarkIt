'''
    Version - 1.0
    Date - 03/02/2020
    
    Script function -
    This script consists of functions to insert and update similarity information in the database.

    Updated: 08/03/2020
    Modified to maintain the running mean.
'''

from app.blue.utils.findsimilar import calc_cosineSimilarity, compare_embeddings
from app.blue.utils.load_embeddings import query_para_embeddings
from app.blue.utils.query_database import query_similarity_info, update_similar, insert_database, query_similarity_info_one, remove_document
from app.blue import collection
from app.config import cfg
import numpy as np


def insert_similarity2(obj_id, sim_ids, page_no, query_id):
    '''
        Function to insert the similarity information along with the embedding information.
    '''
    try:
        # update_similar({"_id": obj_id, "type": "similar_embeddings"}, {"$set": {"sim_ids": sim_ids}})
        # collection.update_one({"_id": obj_id, "type": "similar_embeddings"}, {"$set": {"sim_ids": sim_ids}})
        # refFlag = False

        # query the similarity
        query = {"type": "similarity", "ref_id": obj_id}
        query_answer = query_similarity_info(query)

        sim_ids.append(query_id)
        updateFlag = False

       # update the reference document
        for answer in query_answer:
            pno = answer["page_no"]
            pno.append(page_no)
            pids = answer["sim_ids"]
            pids.extend(sim_ids)
            similarity_id = answer["similarity_id"]
            similarity_id.append(query_id)
            update_similar({"type": "similarity", "ref_id": obj_id}, {"$set": {"page_no": pno, "sim_ids": pids, "similarity_id": similarity_id}})  # update the document in the collection 
            updateFlag = True

        if not updateFlag:
            # insert the reference into the database.
            query = {"type": "similarity", "ref_id": obj_id, "page_no": [page_no], "sim_ids": sim_ids, "similarity_id": [query_id]}
            _ = insert_database(query)

    except Exception as e:
        print("Error: ", e)
        print("Error inserting similarity array to database.")


def update_similarity(query_id, similarity_id): # should this be done by a celery job?
    '''
        Function to update the similarity information for the query in the database.
        
        Arguments:
        :queryid - Paragraph id
        :similarity_id - Similarity ids
    '''
    try:
        query = {"type": "similarity", "para_id": query_id}         # query for similarity
        similarity_answer = query_similarity_info_one(query)        # find one returns a single document.
        
        try:
            similarity_answer = similarity_answer['similarity_id']
            if not similarity_answer: similarity_answer = []
        except:
            print("Error while finding the similarity from the cursor")
            similarity_answer = []
        
        # values to be updated.
        similarity_answer.extend(similarity_id)
        similarity_values = {"$set": {"similarity_id": similarity_answer}}
        collection.update_one(query, similarity_values)             # update the collection with new similarity ids.
    except Exception as e:
        print("Error updating similarity array to database.")
        print("Error: ", e)


def insert_update_fav_embeddings(para_embed, query_id, thresh):
    '''
        Function to insert and update stored favorite embeddings.

        Parameters:
        :para_embed - Embeddings for a paragraph
        :query_id: Paragraph id
        :thresh: Threshold for similarity
    '''
    try:
        query = {
            "type": "similar_embeddings"
        }
        query_answer = query_similarity_info(query)

        foundFlag = False

        # check for similarity with each embedding matrix.
        for answer in query_answer:
            similar_embed = np.array(answer["avg_embeddings"])

            # update the mean embeddings in the db.
            if similar_embed.shape[0]!=para_embed.shape[0]:
                avg_embeddings = query_para_embeddings(answer["similarity_id"]) # fetch the embeddings of all paragraphs in the similarity id and compute the mean.
                similar_embed = np.mean(avg_embeddings, axis=0)
                # collection.update_one({"_id": answer["_id"], "type": "similar_embeddings"}, {"$set": {"avg_embeddings": similar_embed}})
                update_similar({"_id": answer["_id"], "type": "similar_embeddings"}, {"$set": {"avg_embeddings": similar_embed.tolist()}})

            similar_embed=similar_embed.reshape(1, -1) # reshape the embeddings
            para_embed=para_embed.reshape(1, -1)

            assert similar_embed.shape[1]==para_embed.shape[1]
            print("Embeddings: ", (1-calc_cosineSimilarity(similar_embed, para_embed)))

            # check if the new paragraph looks identical to some already stored embeddings.
            if (1-calc_cosineSimilarity(similar_embed, para_embed)) >= thresh:
                prev_sims = answer["similarity_id"]
                prev_len = len(prev_sims)
                similar_embed = ((similar_embed*prev_len)+para_embed) / (prev_len+1)    # maintain the running average
                prev_sims.append(query_id)                                              # update the collection
                updated_embeddings = {"$set": {"similarity_id": prev_sims, "avg_embeddings": similar_embed.tolist()}}
                ret_id = answer["_id"]
                # collection.update_one({"_id": ret_id}, updated_embeddings)              # update the collection with new average embedding
                update_similar({"_id": ret_id}, updated_embeddings)
                foundFlag = True                                                        # if the embeddings are close to some already stored embeddings, update the average embeddings.
                break

        if not foundFlag:
            # ret_id = collection.insert({"type": "similar_embeddings", "avg_embeddings": para_embed.tolist(), "similarity_id": [query_id], "sim_ids": sim_ids})
            ret_id = insert_database({"type": "similar_embeddings", "avg_embeddings": para_embed.tolist(), "similarity_id": [query_id]})
        else:
            para_embed = similar_embed

        return para_embed, ret_id # para_embed will be the same as input to the function, if it is not within a threshold.

    except Exception as e:
        print("Error while inserting/updating embeddings in database.")
        print("Error: ", e)


def de_favoritize2(query_id): # should this be done by a celery job?
    '''
        Function to de-favoritize a paragraph.

        Arguments:
        query_id: query id of the paragraph to be marked not as favorite.

        Returns the list of paragraphs similar to the query and updates the database.
    '''
    try:
        similarity_id = []
        query = {
            "type": "similarity"
        }
        query_answer = query_similarity_info(query)

        similarity_id = []
        similarity_set = set()
        
        for document in query_answer:
            sim_ids = document["sim_ids"]

            if query_id in sim_ids: # if the query id is in the list of similar paragraphs.
                if query_id in document["similarity_id"]: # if the query id is the same as previously favoritized.
                    query = {"_id": document["ref_id"], "type": "similar_embeddings"}
                    doc = query_similarity_info_one(query)
                    doc_similar = doc["similarity_id"]
                    doc_similar.remove(query_id) # remove the queried id
                    psim_ids = sorted(sim_ids) # sort the similar ids.
                    
                    plen = len(doc_similar)
                    if plen>=1:
                        # this will always be an embedding for a single query.
                        query_embedding = query_para_embeddings([query_id]) # query embedding 
                        avg_embeddings = document["avg_embeddings"]
                        updated_embedding = (avg_embeddings * (plen+1) - query_embedding) / plen

                        # update the embeddings
                        update_similar(query, {"$set": {"similarity_id": doc_similar, "avg_embeddings": updated_embedding}})

                        # find the records close to the query embedding and remove those. returns the index.
                        rem_sim_ids = compare_embeddings(query_para_embeddings(psim_ids), query_embedding, updated_embedding) 

                        # also remove the query id from both sim_ids and similarity ids.
                        remove_sids = set()
                        remove_sids.update([psim_ids[s] for s in rem_sim_ids])
                        for sid in remove_sids:
                            psim_ids.remove(sid)
                        update_similar({"_id": document["_id"]}, {"$set": {"sim_ids": psim_ids, "similarity_id": doc_similar}})
                        update_similar({"_id": document["ref_id"]}, {"$set": {"similarity_id": doc_similar}})

                        similarity_id = list(remove_sids) # one that needs to be deselected. again check for similarities in other lists.

                    else: # if single record
                        # delete the record.
                        remove_document(query)
                        remove_document({"_id": document["_id"]})

                    # delete the reference record.
                    
                else: # if query id is present in the sim_ids but nor selected by the user explicitely.
                    sim_ids.remove(query_id)
                    # just update the record.
                    update_similar({"_id": document["_id"]}, {"$set": {"sim_ids": sim_ids}})
            else: 
                similarity_set.update(document["sim_ids"])           # add the similarity ids to the set.

            #     # find the running mean (new embedding to be updated in the db)
            #     psimilarity_id = document["similarity_id"]
            #     avg_embeddings = document["avg_embeddings"]
            #     psim_ids = document["sim_ids"]
            #     psim_ids = sorted(psim_ids) # sort the similar ids.
            #     plen = len(psimilarity_id)
                
            #     # check similarity ids.
            #     similarity_id = []
            #     if plen>1:
            #         updated_embedding = (avg_embeddings * plen - query_embedding)/(plen-1)
            #         # check if psim_ids is not null.
            #         if psim_ids:
            #             sim_ids = compare_embeddings(query_para_embeddings(psim_ids), query_embedding, updated_embedding) # return all ids that are closer to the queried embedding than the average.
            #             for sid in sim_ids:
            #                 similarity_id.append(psim_ids[sid])

            #         sim_ids = [x for x in psim_ids if x not in similarity_id]
            #         print("updated ids: ", sim_ids)
            #         psimilarity_id.remove(query_id)
            #         similarity_updt = {"$set": {"sim_ids": sim_ids, "similarity_id": psimilarity_id, "avg_embeddings": updated_embedding}}
            #         collection.update_one({"_id": document["_id"],"type": "similar_embeddings"}, similarity_updt) 
            #         print("updated!")
            #     else:
            #         if psim_ids: similarity_id.extend(psim_ids)
            #         else: import pdb; pdb.set_trace() 
            #         collection.remove({"_id": document["_id"], "type": "similar_embeddings"})

            #     print("similarity ids: ", similarity_id)
            #     delFlag = True
            
            # # delete the query id from similarity ids.
            # if query_id in document["sim_ids"]:
            #     sim_ids = document["sim_ids"]
            #     sim_ids.remove(query_id)
            #     similarity_updt = {"$set": {"sim_ids": sim_ids}}
            #     collection.update_one({"_id": document["_id"],"type": "similar_embeddings"}, similarity_updt) 
            #     print("updated!")
            #     update_stored_similarity()
            #     if not delFlag: similarity_id = [] # we need to maintain similarity list for paragraphs similar to the given paragraph if it was already calculated.

        # check if the similar paragraph ids are in the similarity_list elsewhere.
        sim_ids = similarity_id
        
        for sid in sim_ids:
            try:
                # check if the id is present somewhere in the similarity list or list of similar paragraphs.
                if sid in similarity_set:
                    similarity_id.remove(sid)
            except:
                print("Trying to remove element not present in the list.")
                continue

        print("similar ids: ", similarity_id)
        return similarity_id
    except Exception as e:
        print("Error: ", e)
        print("Error while defavoritizing paragraphs.")

