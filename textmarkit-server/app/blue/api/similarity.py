from flask import request, redirect, url_for
from flask_restful import Resource
from app.config import cfg
from app.blue.utils.findsimilar import cosine_similar
from app.blue.utils.load_embeddings import query_embeddings
from app.blue.utils.insert_update_similarity import insert_similarity2, de_favoritize2, insert_update_fav_embeddings
from app.blue.utils.query_database import query_similarity_info_one
import traceback

class Similarity(Resource):
    '''
        Controller for api/similarity.
    '''
    def __init__(self):
        pass

    def get(self):
        print("I am in GET.")
        return redirect(url_for('site.homepage'))
        
    def post(self):
        '''
            Computes the similarity of paragraphs.
            
            :return: 
            list of similar paragraphs. 
        '''
        print("Computing similarity!!")
        try:
            try:
                page_no = int(request.form['pageno'])
            except:
                print("Page no field not found in the request.")
                return redirect(url_for('site.pagenotfound'))

            try:
                para_id = int(request.form['para_id'])
            except:
                print("Paragraph no not found in the request.")
                return redirect(url_for('site.pagenotfound'))

            per_page = int(cfg.PER_PAGE)
            limit = per_page*page_no
            start_id = per_page*(page_no-1)
            query_id = start_id+para_id
            end_id = per_page*page_no
                      
            embeddings = []
            while len(embeddings)==0:
                try:
                    # we don't want to query all the paragraphs till that page together.
                    # embeddings = query_embeddings(limit, 0) # query the embeddings of all the page before the current page.
                    embeddings = query_embeddings(per_page, start_id)    # query all the embeddings for the current page.
                except Exception as e:
                    print("Error while querying the embeddings from the db. Error info: ", e)
                
                if len(embeddings)==0:
                    print(query_id)

            # embedding matrix will start from 0, whereas the query_id for para 1 will be 0.
            query = embeddings[query_id-start_id-1] # embeddings of the query 

            # compare the embeddings with other similarities already stored in database.
            query, obj_id = insert_update_fav_embeddings(query, query_id, cfg.SIMILARITY_UPDATE_THRESH)

            # find the previous similarity ids.
            prevsim_ids = query_similarity_info_one({"ref_id": obj_id, "type": "similarity"})
            if prevsim_ids:
                prevsim_ids = prevsim_ids["sim_ids"]
            else: prevsim_ids = []

            # return ids of similar paragraphs till the current page.
            sim_ids = cosine_similar(query_id, query, embeddings, cfg.TOP_THRESHOLD)
            prevsim_ids.extend([x+start_id for x in sim_ids])
            prevsim_ids = list(set(prevsim_ids))

            print("sim_ids: ", prevsim_ids)

            try:
                # insert_similarity(query_id, sim_ids) # insert the similarity of the paragraphs for future use.
                insert_similarity2(obj_id, prevsim_ids, page_no, query_id)         # update the similarity information.
                print("Records inserted into the database.")
            except:
                print("Error while inserting records.")
            
            return ['button-'+str(x-start_id) for x in sim_ids]
            # return ['button-'+str(x-start_id) for x in sim_ids if start_id+1<=x<=end_id]
        except Exception as e:
            print("Error: ", e)
            print("oh crap! error!")
            print(traceback.format_exc())
            return self.redirect()

    def redirect(self):
        print("In redirect!")
        return redirect(url_for('errors.handle_error'))

class DeleteSimilarity(Resource):
    '''
        Controller for api/delete_similarity.
    '''
    def __init__(self):
        pass

    def get(self):
        print("I am in GET.")
        return redirect(url_for('site.homepage'))
        
    def post(self):
        '''
            API used to handle the user defavoritizing a paragraph.
            Update the favorite flag in the database.

            :return: 
            list of paragraphs that should also be defavoritized. 
        '''
        try:
            try:
                page_no = int(request.form['pageno'])
            except:
                print("Page no field not found in the request.")
                return redirect(url_for('site.pagenotfound'))

            try:
                para_id = int(request.form['para_id'])
            except:
                print("Paragraph no not found in the request.")
                return redirect(url_for('site.pagenotfound'))
            
            per_page = int(cfg.PER_PAGE)
            start_id = per_page*(page_no-1)
            query_id = start_id+para_id
            end_id = per_page*page_no

            # sim_ids=de_favoritize(query_id)
            sim_ids=de_favoritize2(query_id)

            return ['button-'+str(x-start_id) for x in sim_ids if start_id<x<=end_id]
        except Exception as e:
            print("Error: ", e)
            print("oh crap! error!")
            print(traceback.format_exc())
            return self.redirect()

    def redirect(self):
        print("In redirect!")
        return redirect(url_for('errors.handle_error'))
