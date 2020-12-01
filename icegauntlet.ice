module IceGauntlet  {
    exception Unauthorized{ string error;};
    exception RoomAlreadyExists{string error;};
    exception RoomNotExists{string error;}; 


    interface Authentication{ 
        bool isValid (string token) throws Unauthorized; 
        string getNewToken (string user , string passHash) throws Unauthorized;
        void changePassword(string user , string currentPassHash, string newPassHash) throws Unauthorized;

    };

    interface Server{
        string getRoom() throws RoomAlreadyExists;
        void Publish(string token, string roomData);
        void Remove(string token , string roomName)  throws RoomNotExists;
    };



};