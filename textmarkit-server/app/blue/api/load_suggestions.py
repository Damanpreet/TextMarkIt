from flask import request, redirect, url_for
from flask_restful import Resource
from app.blue.utils.findsimilar import cosine_similar
from app.config import cfg
from app.blue.utils.load_embeddings import query_embeddings, query_para_embeddings
from app.blue.utils.query_database import query_similarity_info, update_similar, query_similarity_info_one
import traceback
import numpy as np

class LoadSuggestions(Resource):
    '''
        Controller for api/load_suggestions.
    '''
    def __init__(self):
        pass

    def get(self):
        print("I am in GET.")
        return redirect(url_for('site.homepage'))
        
    def post(self):
        '''
            Load the similarity suggestions when the new page is loaded.
            
            :return: 
            list of similar paragraphs. 
        '''
        try:
            try:
                page_no = int(request.form['pageno'])
            except:
                print("Page no field not found in the request.")
                return redirect(url_for('site.pagenotfound'))

            per_page = int(cfg.PER_PAGE)
            start_id = per_page*(page_no-1)
            end_id = start_id+per_page

            print("Page no: ", page_no, "start id: ", start_id, "end_id: ", end_id)

            # load the suggestions
            sim_ids_set = set() # to store the similarity on the current page.
            query_answer = query_similarity_info({"type": "similarity"})

            embeddings = query_embeddings(per_page, start_id) 

            for answer in query_answer:
                psim_ids = answer["sim_ids"]
                pno = answer["page_no"]

                if page_no in pno:
                    sim_ids_set.update([x-start_id for x in psim_ids if start_id < x <= end_id])
                else:
                    # compute the similarity
                    # query_id = answer["similarity_id"]-start_id if start_id < answer["similarity_id"] <= end_id else -1
                    avg_embedding = np.array(query_similarity_info_one({"_id": answer["ref_id"]})["avg_embeddings"])

                    # update the mean embeddings in the db.
                    if avg_embedding.shape[0]!=embeddings.shape[0]:
                        similarity_ids = query_similarity_info_one({"_id": answer["ref_id"]})["similarity_id"]
                        avg_embeddings = query_para_embeddings(similarity_ids) # fetch the embeddings of all paragraphs in the similarity id and compute the mean.
                        avg_embedding = np.mean(avg_embeddings, axis=0)
                        update_similar({"_id": answer["ref_id"]}, {"$set": {"avg_embeddings": avg_embedding.tolist()}}) # update the average embedding information. 

                    sim_ids = cosine_similar(-1, avg_embedding, embeddings, cfg.TOP_THRESHOLD)

                    print("similarity: ", sim_ids)
                    sim_ids_set.update(sim_ids)

                    # update the record - page no and sim_ids
                    psim_ids.extend([x+start_id for x in sim_ids])
                    pno.append(page_no)
                    update_similar({"_id": answer["_id"]}, {"$set": {"page_no": pno, "sim_ids": psim_ids}})

            print("similar suggestions: ", sim_ids_set)
            return ['button-'+str(x) for x in sim_ids_set]
        except Exception as e:
            print("Error: ", e)
            print(traceback.format_exc())
            return self.redirect()

    def redirect(self):
        print("In redirect!")
        return redirect(url_for('errors.handle_error'))
        