from redis_conn import redis_client

class command_handler(object):
    def __init__(self, **sys_args):
        self.sys_args = sys_args
        print(len(self.sys_args),self.sys_args)
        # if len(self.sys_args)<2:
        #     exit(self.help_msg())
        # self.command_allowcator()


    def command_allowcator(self):
        '''分捡用户输入的不同指令'''
        print(self.sys_args[1])

        if hasattr(self,self.sys_args[1]):
            func= getattr(self,self.sys_args[1])
            return func()
        else:
            print("command does not exist!")
            self.help_msg()

    def help_msg(self):
        valid_commands = '''


        '''
        exit(valid_commands)


    def start(self):
        print("going to start the monitor client")
        #exit_flag = False
        #
        # Client = client.ClientHandle()
        # Client.forever_run()

    def stop(self):
        print("stopping the monitor client")


if __name__ == "__main__":
    command_handler()