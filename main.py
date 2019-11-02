from flask import Flask, render_template, make_response, redirect, url_for
from flask_restful import Api, Resource, reqparse
from random import random
from data import update_hostings, read_hostings, html_render

app = Flask(__name__)
api = Api(app)
headers = {'Content-Type': 'text/html'}    

@app.route('/')
@app.route('/index')
def index():
    return make_response(render_template('index.html'), 200, headers)

@app.route('/hostings')
def list_hostings():
    hostings = read_hostings()
    if not hostings: hostings = 'No hay ningun hosting'
    return make_response('<html>'+html_render(hostings)+'</html>', 200, headers)

class HostingHandler(Resource):
    
    def get(self, action):
        if action not in ['create','delete','edit']: return redirect(url_for('index'))
        return make_response(render_template(f'{action}.html'), 200, headers)
    
    def post(self, action):
        if action == 'create':
            args = self.__parse(reqparse.RequestParser())
            if not args['name']: return make_response(render_template('create.html', errorcode='Y el nombre?'), 400, headers)
            
            for hosting in read_hostings():
                if args['name'] == hosting['name']: return make_response(render_template('create.html', errorcode=f"El hosting {args.get('name')} ya existe"), 400, headers)
                
            update_hostings(self.__create(args))
            
            return make_response(render_template('msg.html', msg=f"Hosting {args.get('name')} creado", action='Crear'), 201, headers)
        
        if action == 'delete':
            return self.delete()
        
        if action == 'edit':
            return self.put()
    
    def put(self, action=None):
        args = self.__parse(reqparse.RequestParser())
        if not args['name']: return make_response(render_template('edit.html', errorcode='Y el nombre?'), 400, headers)
        
        hostings = read_hostings()
        hosting = self.__create(args)
        
        for ix in range(len(hostings)):
            if hosting['name'] == hostings[ix]['name']:
                hostings[ix] = hosting
                update_hostings(hostings, 'w')
                return make_response(render_template('msg.html', msg=f"Hosting {hosting.get('name')} modificado", action='Editar'), 200, headers)
        
        update_hostings(hosting)
        return make_response(render_template('msg.html', msg=f"Hosting {hosting.get('name')} no encontrado, se ha creado uno con los datos especificados", action='Editar'), 201, headers)
    
    def delete(self, action=None):
        args = self.__parse(reqparse.RequestParser())
        
        hostings = read_hostings()
        
        for hosting in hostings:
            if args['name'] == hosting['name']:
                hostings.remove(hosting)
                if not hostings: update_hostings("truncate")
                else: update_hostings(hostings, 'w')
                return make_response(render_template('msg.html', msg=f"{args.get('name')} eliminado", action='Eliminar'), 200, headers)
            
        return make_response(render_template('delete.html', errorcode='Hosting no encontrado'), 404, headers)
    
    
    def __parse(self, parser):
        parser.add_argument('name')
        parser.add_argument('cores')
        parser.add_argument('memory')
        parser.add_argument('disc')
        return parser.parse_args()
    
    def __create(self, attr):
        return {
            'id': str(int(random()*10000000)),
            'name': attr.get('name'),
            'cores': attr.get('cores'),
            'memory': attr.get('memory'),
            'disc': attr.get('disc')
            }
    
api.add_resource(HostingHandler, '/manage/<string:action>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
