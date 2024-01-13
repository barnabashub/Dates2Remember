from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import boto3
from datetime import datetime, timedelta
import DatesHark
from boto3.dynamodb.conditions import Key, Attr
import logging
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
api = Api(app)

# AWS DynamoDB configurations
dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-north-1',
    aws_access_key_id='AKIAYH4CNSTBQAJ5LWIH',
    aws_secret_access_key='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'
)
table = dynamodb.Table('dates')

# class DatesResource(Resource):
#     def get(self):
#         return "hell"
#         logging.error("heeeee")
#         print("heeee")
#         try:
#             logging.info("try to get ownerID")
#             ownerID = request.args.get("ownerID")
#             logging.info(ownerID)
#         except Exception as e1:
#             logging.info("did not work")
#         try:
#             response = table.scan(
#                 FilterExpression=Attr('ownerID').eq(ownerID)
#             )
#             items = response.get('Items', [])
#             items.append('alma')
#             return items
#         except Exception as e:
#             return {'error': str(e)}
        
#     def post(self):
#         try:
#             data = request.get_json()
#             # Assuming the JSON data contains attributes like 'event_name', 'event_date', 'description'
#             new_item = {
#                 'dateID': data.get('dateID'),
#                 'ownerID': data.get('ownerID'),
#                 'title': data.get('title'),
#                 'type': data.get('type'),
#                 'date': data.get('date')
#             }

#             table.put_item(Item=new_item)
#             return {'message': 'Item added successfully'}, 201
#         except Exception as e:
#             return {'error': str(e)}

class DaysAgoResource(Resource):
    def get(self):
        return "daysagoresource"
        try:
            dateID = request.args.get('dateID')
            result = self.days_ago_from_dateID(dateID)
            return {'days_ago': result}, 200
        except Exception as e:
            return {'error': str(e)}

    def get_date_from_dynamodb(self, dateID):
        response = table.get_item(
            Key={
                'dateID': dateID
            }
        )
        if 'Item' not in response:
            return None
        date_from_dynamodb = response['Item']['date']
        return date_from_dynamodb

    def days_ago_from_dateID(self, dateID):
        current_date = datetime.now()

        date_from_dynamodb = self.get_date_from_dynamodb(dateID)

        if date_from_dynamodb is None:
            return "Nincs ilyen dateID-vel rekord a DynamoDB táblában."

        dateID_date = datetime.strptime(date_from_dynamodb, "%Y-%m-%d")

        delta = current_date - dateID_date
        days_ago = delta.days
        return days_ago

    def jubilee_date(self, dateID, days):
        date_from_dynamodb = self.get_date_from_dynamodb(dateID)

        if date_from_dynamodb is None:
            return "Nincs ilyen dateID-vel rekord a DynamoDB táblában."

        dateID_date = datetime.strptime(date_from_dynamodb, "%Y-%m-%d")

        jubilee_date = dateID_date + timedelta(days=days)
        return jubilee_date.strftime("%Y-%m-%d")

    # Endpoint to get the jubilee date
    def get(self):
        try:
            dateID = request.args.get('dateID')
            days = int(request.args.get('days', 0))  # Default to 0 days if not provided
            result = self.jubilee_date(dateID, days)
            return {'jubilee_date': result}, 200
        except Exception as e:
            return {'error': str(e)}
        
class DatesResource(Resource):
    def get(self):
        try:
            ownerID = request.args.get('ownerID')
            response = table.scan(
                FilterExpression=Attr('ownerID').eq(ownerID)
            )
            items = response.get('Items', [])
            return items
        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            data = request.get_json()
            new_item = {
                'dateID': data.get('dateID'),
                'ownerID': data.get('ownerID'),
                'title': data.get('title'),
                'type': data.get('type'),
                'date': data.get('date')
            }
            table.put_item(Item=new_item)
            return {'message': 'Item added successfully'}, 201
        except Exception as e:
            return {'error': str(e)}

class SingleDateResource(Resource):
    def get(self, dateID):
        try:
            response = table.get_item(
                Key={
                    'dateID': dateID
                }
            )
            if 'Item' not in response:
                return {'error': f'No item found for dateID {dateID}'}, 404
            return response['Item']
        except Exception as e:
            return {'error': str(e)}

    def delete(self, dateID):
        try:
            response = table.delete_item(
                Key={
                    'dateID': dateID
                }
            )
            if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {'message': f'Item with dateID {dateID} deleted successfully'}, 200
            else:
                return {'error': f'Failed to delete item with dateID {dateID}'}, 500
        except Exception as e:
            return {'error': str(e)}
        
class NextGreatDatesResource (Resource):
    def get(self):
        amount = request.args.get('amount')
        ownerID = request.args.get('ownerID')
        #amount = int(request.args.get('amount', 5))
        dates_list = []
        date = datetime.now()
        great_dates = DatesResource.get(self)
        while len(dates_list) < int(amount):
            for great_date in great_dates:
                if DatesHark.DatesHark.any_jubilee(great_date, date):
                    dates_list.append(date.strftime("%Y-%m-%d"))
            date = date + timedelta(days=1)
        return dates_list

# Add resources to the API
api.add_resource(DatesResource, '/d/<user_id>/dates')
api.add_resource(DaysAgoResource, '/d/<user_id>/days_ago_from_dateID', '/d/<user_id>/jubilee_date')
api.add_resource(SingleDateResource, '/d/<user_id>/date/<string:dateID>')
api.add_resource(NextGreatDatesResource, '/d/<user_id>/great_dates')

if __name__ == '__main__':
    app.run(debug=True)
