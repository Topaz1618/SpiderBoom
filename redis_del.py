from redis_conn import redis_client

class Redis_Handle(object):
    def __init__(self):
        self.input_msg = 'Usage: {user:password} >> '
        self.exit_list = ['exit', 'q', 'quit']
        self.redis = redis_client()
        self.website = None
        self.start()

    def start(self):
        msg = ''
        msg_dic = self.msg()
        for k, v in msg_dic.items():
            msg += "{}. {}\n".format(k, v[0])
        aaa = input('enter website >>> ')
        self.website = '{}_account'.format(aaa)
        while True:
            print("当前网站：",self.website)
            choice = input(msg)
            i = [str(i) for i in range(1, 5)]
            if choice in i:
                func = msg_dic[choice][1]
                if hasattr(self,func):
                    g = getattr(self, func)
                    g()
            elif choice in self.exit_list:
                break
            else:
                print("不合法")

    def add_user(self):
        print('a',self.website)
        user = input(self.input_msg)
        a = user.split(':')
        self.redis.hset(self.website,a[0],a[1])

    def del_user(self):
        print("d", self.website)
        user = input('delect user >>>')
        self.redis.hdel(self.website, user)

    def select_user(self):
        print("s",self.website)
        user_msg = '===== 当前用户个数：%s ======\n' %self.redis.hlen(self.website)
        a = self.redis.hgetall(self.website)
        for k, v in a.items():
            s = ' {}: {}\n'.format(k.decode(),v.decode())
            user_msg += s
        print(user_msg)

    def alter_user(self):
        print("a", self.website)
        user = input('user:passwd')
        a = user.split(':')
        self.redis.hset(self.website, a[0], a[1])

    def msg(self):
        msg_dic = {
            '1': ['新增用户', 'add_user'],
            '2': ['修改用户数据', 'alter_user'],
            '3': ['查询当前用户', 'select_user'],
            '4': ['删除用户', 'del_user'],
            '选择数字': ['..退出按q >>>'],
        }
        return msg_dic


if __name__ == "__main__":
    Redis_Handle()


'''
redis 操作： https://www.jianshu.com/p/2639549bedc8
'''