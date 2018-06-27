from redis_conn import redis_client

r = redis_client()
r.delete('weibo_account')

#新增
r.hset("weibo_account", "k1", "v1")
r.hset("weibo_account", "k2", "v2")
r.hset("weibo_account", "k3", "v3")
r.hset("weibo_account","kkk","12312312311")

#显示所有键值
print(r.hgetall('weibo_account'))
a = r.hgetall('weibo_account')
for k,v in a.items():
    print(k.decode(),v.decode())


print(r.hlen("weibo_account")) #显示个数
r.hdel("hash1", "k1")          #删除一个键值对
r.hset("hash1", "k2", "v222")  #修改已有



