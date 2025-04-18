class User {
    constructor(userId, username, password) {
        this.userId = userId;
        this.username = username;
        this.password = password; // In a real application, ensure to hash this
    }

    // Method to validate user credentials
    validateCredentials(inputUsername, inputPassword) {
        return this.username === inputUsername && this.password === inputPassword;
    }
}

export default User;