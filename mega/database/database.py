import os
import datetime
import motor.motor_asyncio
from ...telegram import Common

myclient = motor.motor_asyncio.AsyncIOMotorClient(Common().database_url)
mydb = myclient["FileToLink"]
dmycol = mydb['Users']

def new_user(id):
    return dict(
        id = id,
        join_date = datetime.date.today().isoformat(),
        ban_status=dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
    )
async def add_user(id):
    user = new_user(id)
    await dmycol.insert_one(user)

async def is_user_exist(id):
    user = await dmycol.find_one({'id':int(id)})
    return True if user else False

async def remove_ban(id):
    ban_status = dict(
        is_banned=False,
        ban_duration=0,
        banned_on=datetime.date.max.isoformat(),
        ban_reason=''
    )
    await dmycol.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

async def ban_user(user_id, ban_duration, ban_reason):
    ban_status = dict(
        is_banned=True,
        ban_duration=ban_duration,
        banned_on=datetime.date.today().isoformat(),
        ban_reason=ban_reason
    )
    await dmycol.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

async def get_ban_status(id):
    default = dict(
        is_banned=False,
        ban_duration=0,
        banned_on=datetime.date.max.isoformat(),
        ban_reason=''
    )
    user = await dmycol.find_one({'id':int(id)})
    return user.get('ban_status', default)
    
    
async def get_all_banned_users():
    banned_users = dmycol.find({'ban_status.is_banned': True})
    return banned_users



async def total_users_count():
    count = await dmycol.count_documents({})
    return count

async def get_all_users():
    all_users = dmycol.find({})
    return all_users

async def delete_user(user_id):
    await dmycol.delete_many({'id': int(user_id)})


