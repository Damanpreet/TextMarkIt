'''
    source: https://harishvc.com/2015/04/15/pagination-flask-mongodb/
    Paginate data
'''
from app.blue import collection
import traceback
from app.blue.utils.query_database import query_similarity_info
from flask_restful import Resource
from flask import Response

class ExportFile(Resource):
    '''
        Controller for api/exportfile.
    '''

    def __init__(self):
        pass

    def get(self):
        try:
            '''
                Get request for api/exportfile.
            '''
            print("I am in GET.")

            query_answer = query_similarity_info({"type": "similarity"})

            similarity_ids = set()
            
            for answer in query_answer:
                similarity_ids.update(answer["sim_ids"])

            # sort the list of similarity ids.
            similarity_ids = sorted(list(similarity_ids))

            try:
                query = [
                    {
                        "$match":
                            {
                                "type": "text",
                                "para_id": {
                                    "$in": similarity_ids
                                }
                            }
                    },
                    {
                        "$project" : {
                                "_id" : 0,
                                "text" : 1
                        }
                    },
                    {
                        "$sort": {
                            "_id": 1
                        }
                    }]

                result = collection.aggregate(query)
            except:
                print("Error connecting to database")

            # write a document
            # document = ""
            # for para in result:
            #     document += para["text"] + "\n\n"
            # print(document)

            # write an html file
            document = """
            <html>
            <head>
            <title> Exported File </title>
            </head>
            """
            for para in result:
                document += """
                    <p> """ + para["text"] + """</p> <br>
                """
            document+= """
                </html>
                """ # close the html tag

            # download the file.
            # return send_file('test.doc', as_attachment=True)
            return Response(document, 
                mimetype="text/html",
                headers={"Content-disposition": "attachment; filename=text.html"})
            
            
        except Exception as e:
            print("Error information: ", e)
            print(traceback.format_exc())
            return self.redirect()

    # def post(self):
    #     try:
    #         '''
    #             Post request for api/exportfile.
    #         '''
    #         print("I am in POST.")

    #         query_answer = query_similarity_info({"type": "similarity"})

    #         similarity_ids = set()
            
    #         for answer in query_answer:
    #             similarity_ids.update(answer["sim_ids"])

    #         # sort the list of similarity ids.
    #         similarity_ids = sorted(list(similarity_ids))

    #         # download the file.
    #         return send_file('test.doc', as_attachment=True)
    #     except Exception as e:
    #         print("Error information: ", e)
    #         print(traceback.format_exc())
    #         return self.redirect()

    def redirect(self):
        print("In redirect!")
        return redirect(url_for('errors.handle_error'))

        