'''
    Version - 1.0
    Date - 03/02/2020
    
    Script function -
    This script consists of functions to insert and update similarity information in the database.
'''

from app.blue import collection
import numpy as np


def check_similarity(query_id): 
    '''
        Function to check if the paragraph is already in the favorite list.
        If it's present, favoritize it again.
    '''
    try:
        query = {"type": "similarity", "para_id": query_id}
        answer = collection.find_one(query)
        
        if answer:
            # check if it's not favorite, favoritize it.
            if not answer["favorite"]:
                similarity_flag = {"$set": {"favorite": True}}
                collection.update(query, similarity_flag)
                return True, answer["similarity_id"]
        return False, []
    except Exception as e:
        print("Error while fetching similar paragraphs stored in the database.")
        print("Error: ", e)


def insert_similarity(query_id, similarity_id):
    '''
        Function to insert the similarity information for the query in the database.
    '''
    try:
        collection.insert({"type": "similarity", "para_id": query_id, "similarity_id": similarity_id, "favorite": True})
    except Exception as e:
        import pdb; pdb.set_trace()
        print("Error: ", e)
        print("Error inserting similarity array to database.")


def update_similarity(query_id, similarity_id): # should this be done by a celery job?
    '''
        Function to update the similarity information for the query in the database.
    '''
    try:
        query = {"type": "similarity", "para_id": query_id} # query for similarity
        
        similarity_answer = collection.find_one(query) # find one returns a single document.
        
        try:
            similarity_answer = similarity_answer['similarity_id']
            if not similarity_answer: similarity_answer=[]
        except:
            print("Error while finding the similarity from the cursor")
            similarity_answer = []
        
        # values to be updated.
        similarity_answer.extend(similarity_id)
        similarity_values = {"$set": {"similarity_id": similarity_answer}}
        
        collection.update_one(query, similarity_values) # update the collection with new similarity ids.
    except Exception as e:
        print("Error updating similarity array to database.")
        print("Error: ", e)


def de_favoritize(query_id): # should this be done by a celery job?
    '''
        Function to de-favoritize a paragraph.
    '''
    try:
        similarity_id = []
        query = {"type": "similarity", "para_id": query_id} # query for similarity
        answer = collection.find_one(query)
        print("answer:  ", answer)
        if answer and "favorite" in answer and answer["favorite"]:
            try:
                similarity_flag = {"$set": {"favorite": False}} 
                collection.update_one(query, similarity_flag) # update the similarity flag if it's the root.
                print("updated!")
                similarity_id = answer["similarity_id"]
            except Exception as e:
                print("error while  updating the collection in de_favoritize.")
                print("error: ", e)

        query_sim = {"type": "similarity"}
        answer_sim = collection.find(query_sim)

        # update the similar paragraphs if the query id is present in the para similarity for other paras.
        for ans in answer_sim:
            if query_id in ans['similarity_id']:                
                try: # fetch the similarity ids and remove the query id.
                    similar_p = ans["similarity_id"]
                    similar_p.remove(query_id)
                except:
                    print("Exception while removing similarity id.")
                
                similarity_updt = {"$set": {"similarity_id": similar_p}}
                # update the records with the query id removed.
                try: 
                    collection.update_one({"type": "similarity", "para_id": ans["para_id"]}, similarity_updt)
                    print("Collection updated!")
                except:
                    print("Error while updating the collection.")
            
        
        return similarity_id
    except Exception as e:
        print("Error: ", e)
        print("Error while defavoritizing paragraphs.")

# def check_favourites():
#     '''
#         Check paragraph ids which are favoritized.

#         returns:
#         paragraph ids of already favoritized text.
#     '''
#     # query all paragraphs which were favoritized.
#     query = {"type": "similarity", "favorite": True}
#     answer = collection.find(query)
    
#     sim_ids = []
#     for ans in answer:
#         sim_ids.append(ans["para_id"])
    
#     return sim_ids

def check_favourites():
    '''
        Check paragraph ids which are favoritized.

        returns:
        paragraph ids of already favoritized text.
    '''
    # query all paragraphs which were favoritized.
    query = {"type": "similarity", "favorite": True}
    return collection.find(query)
