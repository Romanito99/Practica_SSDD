# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
import hashlib
import json
import argparse
import getpass
import Ice
Ice.loadSlice('icegauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

class ClientAuth(Ice.Application):
    '''This Class permit us authenticate our user'''
    def compute_hash(self,filename):
        '''This method encrypt our password'''
        file_hash = hashlib.sha256()
        file_hash.update(filename.encode())
        return file_hash.hexdigest()

    def new_password(self):
        '''This method let us introduce the new password'''
        print("Enter new password")
        new_hash = getpass.getpass("Enter password>")
        new_hash= self.compute_hash(new_hash)
        return new_hash

    def actual_password(self):
        '''This method let us introduce the password'''
        print("Enter password")
        hash = getpass.getpass("Enter password>")
        hash= self.compute_hash(hash)
        return hash

    def args_parser(self):
        '''This method is for the parser'''
        description = 'Choose Proxy, user and option: 1.Change Password 2.New Token'
        parser = argparse.ArgumentParser(description)
        parser.add_argument("-p","--proxy",required=True, help='proxy',type=str)
        parser.add_argument("-u","--user",required=True,help='user',type=str)
        parser.add_argument("-o","--option",required=True,help='option',type=str)
        args=parser.parse_args()
        return args
    def run(self):
        '''This method is our main'''
        args = self.args_parser()
        proxy=args.proxy
        user=args.user
        opcion=args.option
        broker=self.communicator()
        proxy_authserver=broker.stringToProxy(proxy)
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy_authserver)

        if not authserver:
            raise RunTimeError('Invalid Proxy')
        try:
            with open("users.json") as file:
                user_data=file.read()
            user_data=json.loads(user_data)
        except:
            print("File can't be read")
        else:
            user_name = user_data[user]
            if len(user_name)==0:
                new_hash = self.new_password()
                authserver.changePassword(str(user),None,str(new_hash))
                print('"{}"'.format(user_name["current_token"]), flush=True)
            else:
                hash = self.actual_password()
                current_hash = user_name["password_hash"]
                if current_hash == hash  :
                    print("User Valid\n ")
                    if opcion == "1":
                        new_hash = self.new_password()
                        authserver.changePassword(user, current_hash ,new_hash)
                        print('"{}"'.format(user_name["current_token"]), flush=True)
                    elif opcion == "2":
                        token=authserver.getNewToken(user,current_hash)
                        print('"{}"'.format(token), flush=True)
                else:
                    print("User not valid or password not correct\n ")

ClientAuth().run()
 