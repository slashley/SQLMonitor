import pysnow
import yaml

# Import config
with open('./config/config.yml', 'r') as ymlconfig:
    theconfig = yaml.load(ymlconfig)

# get all open (New[1] and Active[2]) incidents for a specific CI mathcing a specific subcategory
def getincidentbyci(ci, subcat):
    c = pysnow.Client(instance=theconfig['snowinstance'], user=theconfig['snowusername'], password=theconfig['snowpassword'])
    incidents = c.resource(api_path='/table/incident')
    qb = (
        pysnow.QueryBuilder()
        .field('cmdb_ci.sys_id').equals(ci)
        .AND()
        .field('subcategory').equals(subcat)
        .AND()
        .field('incident_state').equals('1')
        .OR()
        .field('incident_state').equals('2')
    )
    response = incidents.get(query=qb, fields=['sys_id','number'])
    return response.all()

# get CI by 'name', requires an exact match, more than 1 or none results in error
def getcibyname(ciname):
    c = pysnow.Client(instance=theconfig['snowinstance'], user=theconfig['snowusername'], password=theconfig['snowpassword'])
    configitem = c.resource(api_path='/table/cmdb_ci_server')
    response = configitem.get(query={'name': ciname}, fields=['company', 'company.u_clientid', 'name', 'sys_id', 'operational_status', 'u_service_plan'])
    return response.one_or_none()

# create an incident record
def createincident(configitem, company, priority, urgency, impact, category, subcategory, description, assignment):
    c = pysnow.Client(instance=theconfig['snowinstance'], user=theconfig['snowusername'], password=theconfig['snowpassword'])
    incident = c.resource(api_path='/table/incident')
    inc_record = {
        'cmdb_ci': configitem,
        'company': company,
        'priority': priority,
        'urgency': urgency,
        'impact': impact,
        'category': category,
        'subcategory': subcategory,
        'short_description': description,
        'assignment_group': assignment
    }
    new_record = incident.create(payload=inc_record)
    return new_record

def getactivecitasks(ci):
    c = pysnow.Client(instance=theconfig['snowinstance'], user=theconfig['snowusername'], password=theconfig['snowpassword'])
    changetasks = c.resource(api_path='/table/task_ci')
    qb = (
        pysnow.QueryBuilder()
        .field('ci_item.sys_id').equals(ci)
        .AND()
        .field('task.sys_class_name').equals('change_request')
        .AND()
        .field('task.state').equals('4')
    )
    response = changetasks.get(query=qb, fields=['sys_id','task.number', 'ci_item'])
    return response.all()
