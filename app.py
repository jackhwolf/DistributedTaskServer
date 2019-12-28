from flask import Flask
from flask_restplus import Resource, Api, reqparse
import time
from uuid import uuid4
from TaskMngr import TaskMngr
from distributed import Client

if __name__ == '__main__':  # this is nec. to use the Client like we do
    tm  = TaskMngr()
    app = Flask(__name__)
    api = Api(app, title='DistributedTasks API', prefix='/v1')
    cli = Client()
    
    @api.route('/test')
    class test(Resource):
        ''' test that the app/api is running'''

        def get(self):
            return {'test': str(int(time.time()*1000))}

    @api.route('/task')
    @api.route('/task/<tid>')
    class task(Resource):
        ''' for task operations '''

        def post(self):
            ''' submit a new task to be executed and tracked '''
            parser = reqparse.RequestParser()
            parser.add_argument('task', required=1, help='Name of task function to submit.')
            args = parser.parse_args()
            tid, msg = tm.submitTask(cli, args.task)
            return {'tid': tid, 'message': msg}
        
        def get(self, tid):
            ''' get result of task if finished, or the task status '''            
            resp = {}
            resp['status'] = tm.getTaskStatus(tid)
            if resp['status'] == 'finished':
                resp['result'] = tm.getTaskResult(cli, tid)
            return resp

    app.run(debug=True)
        