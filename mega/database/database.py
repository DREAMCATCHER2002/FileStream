import datetime
import motor.motor_asyncio

from sample_config import Config

class Db:
    
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(self.dburl)
        self.db = self._client["RenameDXBot"]
        self.col = self.db.users
        self.thumb = self.db.thumbnail
        self.lang = self.db.LANGUAGE
    
    
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat(),
            caption=None,
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return True if user else False
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count    
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    
    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})
    
    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        return user.get('ban_status', default)
    
    
    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users 
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

