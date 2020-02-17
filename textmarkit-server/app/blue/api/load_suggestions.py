from flask import request, redirect, url_for
from flask_restful import Resource
from app.blue.utils.findsimilar import cosine_similar
from pymongo import MongoClient
from app.config import cfg
from app.blue.utils.load_embeddings import query_embeddings
from app.blue.utils.insert_update_similarity import check_favourites, update_similarity
import traceback

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

            try:
                identifier = request.form['identifier']
            except:
                print("Identifier not found in the request.")
                print("Considering default identifier next.")
                identifier = "next"

            per_page = int(cfg.PER_PAGE)
            start_id = per_page*(page_no-1)
            end_id = start_id+per_page

            print("Page no: ", page_no, "start id: ", start_id, "end_id: ", end_id)

            # check the favorites on the next button click.
            if identifier == "next":
                # find the favoritized paragraphs from the database.
                answer = check_favourites()
                similarp = set()
                for ans in answer:
                    similarp.add(ans["para_id"])

                embeddings = query_embeddings(per_page, start_id) # query the embeddings of all the page before the current page.

                # find the page similarity ids.
                sim_ids_page = set()
                for p in similarp:                            
                    query = query_embeddings(1, p-1)

                    # find ids of similar paragraphs on the page.
                    sim_ids = cosine_similar(p, query, embeddings, cfg.TOP_THRESHOLD)

                    # update the similarp similarity list to be sent back to the browser.
                    sim_ids_page.update(sim_ids)

                    # update the similarity list in the database.
                    update_similarity(p, [sid+start_id for sid in sim_ids])

            else: 
                # For the previous page similarity is already calculated.
                # Fetch the favorite paragraphs from the database.
                answer = check_favourites()
                
                # fetch the paragraphs to be highlighted on the current page.
                sim_ids_page = set()
                for ans in answer:
                    if start_id<ans['para_id']<=end_id:
                        sim_ids_page.add(ans['para_id']-start_id)
                    
                    print([x for x in ans['similarity_id'] if start_id<x<=end_id])
                    # find the similar paragraphs on the current page.
                    sim_ids_page.update([x-start_id for x in ans['similarity_id'] if start_id<x<=end_id])

            print(['button-'+str(x) for x in sim_ids_page])
            return ['button-'+str(x) for x in sim_ids_page]
        except Exception as e:
            print("Error: ", e)
            print(traceback.format_exc())
            return self.redirect()