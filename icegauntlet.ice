module IceGauntle  {
    exception Unauthorized{string error};
    exception RoomAlreadyExists{string error};
    exception RoomNotExists{string error}; 

    interface AuthSever {
        bool isValid (string token) thorws Unauthorized; 
        string getNewToken (string user , string passHash) throws Unauthorized;
        void changePassword(string user , string currentPassHash, string newPassHash) trhows Unauthorized

    } 

    interface Server {
        string getRoom() thorws RoomAlreadyExists;
        void Publish(string token, string roomData);
        void Remove(string token , string roomName)  trhows RoomNotExists;
    }



}