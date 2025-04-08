require('dotenv').config();
const {Storage} = require('@google-cloud/storage');

const storage = new Storage({
    projectId: process.env.GOOGLE_CLOUD_PROJECT_ID,
    credentials: JSON.parse(
        Buffer.from(process.env.GOOGLE_CLOUD_CREDENTIALS, 'base64').toString()
    )
});

const bucketName = 'premiumdownloads-files'; // Deberás crear este bucket en Google Cloud Console

const storageManager = {
    async uploadFile(filePath, destination) {
        try {
            await storage.bucket(bucketName).upload(filePath, {
                destination: destination,
            });

            const url = `https://storage.googleapis.com/${bucketName}/${destination}`;
            return url;
        } catch (error) {
            console.error('Error al subir archivo:', error);
            throw error;
        }
    },

    async getSignedUrl(filename) {
        try {
            const options = {
                version: 'v4',
                action: 'read',
                expires: Date.now() + 15 * 60 * 1000, // 15 minutos
            };

            const [url] = await storage
                .bucket(bucketName)
                .file(filename)
                .getSignedUrl(options);

            return url;
        } catch (error) {
            console.error('Error al generar URL firmada:', error);
            throw error;
        }
    }
};

module.exports = storageManager;