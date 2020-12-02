module IceGauntlet  {
    exception Unauthorized{ string error;};
    exception RoomAlreadyExists{string error;};
    exception RoomNotExists{string error;}; 
    exception WrongRoomFormat {};

    interface Authentication{ 
        bool isValid (string token) throws Unauthorized; 
        string getNewToken (string user , string passHash) throws Unauthorized;
        void changePassword(string user , string currentPassHash, string newPassHash) throws Unauthorized;

    };

    interface Server{
        string getRoom() throws RoomNotExists;
        void Publish(string token, string roomData) throws Unauthorized, RoomAlreadyExists, WrongRoomFormat;
        void Remove(string token , string roomName)  throws Unauthorized, RoomNotExists;
    };



};