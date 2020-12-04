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

    interface RoomManager{
        void publish(string token, string roomData) throws Unauthorized, RoomAlreadyExists, WrongRoomFormat;
        void remove(string token , string roomName)  throws Unauthorized, RoomNotExists;
    };
    interface Dungeon {
        string getRoom() throws RoomNotExists;
    };



};