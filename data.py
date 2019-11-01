from ast import literal_eval

def update_hostings(hosting, mode='a'):
    if hosting == 'truncate':
        with open('hostings.txt', 'w') as hostings:
            hostings.truncate(0)
        return
    
    if type(hosting) is list:
        with open('hostings.txt', mode) as hostings:
            for h in hosting: hostings.write(str(h)+'\n')
        return
            
    with open('hostings.txt', mode) as hostings:
        hostings.write(str(hosting)+'\n')
        
def read_hostings():
    with open('hostings.txt', 'r') as hostings:
        hosting_list = hostings.read().splitlines()
        
    return [literal_eval(hosting) for hosting in hosting_list]
    
def html_render(data):
    if type(data) is dict:
        return f"<p>ID: {data.get('id')}<br>"+\
               f"Nombre: {data.get('name')}<br>"+\
               f"Cores: {data.get('cores')}<br>"+\
               f"Memoria: {data.get('memory')}<br>"+\
               f"Disco: {data.get('disc')}</p>"
    
    elif type(data) is list:
        st = ""
        for e in data:
            st += html_render(e)
            
        return st
    
    else: return data