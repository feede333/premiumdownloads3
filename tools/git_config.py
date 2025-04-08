import os
import subprocess
import base64

def setup_git_credentials():
    try:
        # GitHub token desde variable de entorno
        token = os.getenv("GITHUB_TOKEN")
        
        # Get the repository root directory
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        print(f"Configurando Git en: {repo_dir}")
        
        # Configure Git credentials
        subprocess.run(['git', 'config', '--global', 'user.name', 'feede333'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'your.email@example.com'], check=True)
        
        # Set up credential helper to store the token
        subprocess.run(['git', 'config', '--global', 'credential.helper', 'store'], check=True)
        
        # Configure the remote with token embedded in URL
        repo_url = f"https://x-access-token:{token}@github.com/feede333/premiumdownloads2.git"
        subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], 
                      cwd=repo_dir, check=True)
        
        print("✅ Git configurado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando Git: {str(e)}")
        return False

if __name__ == "__main__":
    setup_git_credentials()