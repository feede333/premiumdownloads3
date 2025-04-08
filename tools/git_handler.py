import os
import subprocess
import json

class GitHandler:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.token = os.getenv("GITHUB_TOKEN")  # Usar variable de entorno
        self.setup_git()

    def setup_git(self):
        try:
            # Set the token in the URL
            repo_url = f"https://{self.token}@github.com/feede333/premiumdownloads2.git"
            
            # Configure Git
            subprocess.run(['git', 'config', '--global', 'user.name', 'feede333'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'your.email@example.com'], check=True)
            subprocess.run(['git', 'config', '--global', 'credential.helper', 'store'], check=True)
            
            # Set remote URL with token
            subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], 
                         cwd=self.repo_dir, check=True)
            
            print("✅ Git configurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando Git: {e}")
            return False

    def push_changes(self, message):
        try:
            # Add specific files
            subprocess.run(['git', 'add', 'data/programs.json'], 
                         cwd=self.repo_dir, check=True)
            subprocess.run(['git', 'add', 'images/*'], 
                         cwd=self.repo_dir, check=True)
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', message], 
                         cwd=self.repo_dir, check=True)
            
            # Push using token in URL
            repo_url = f"https://{self.token}@github.com/feede333/premiumdownloads2.git"
            subprocess.run(['git', 'push', repo_url, 'main'], 
                         cwd=self.repo_dir, check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en Git: {e}")
            return False