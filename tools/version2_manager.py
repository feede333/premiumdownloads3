import os
from tkinter import *
from tkinter import ttk, messagebox
import re
import subprocess
try:
    from git import Repo
except ImportError:
    messagebox.showerror("Error", "GitPython no está instalado. Por favor ejecute: pip install GitPython")
    raise

class VersionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Versiones")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Directorio donde están los archivos details.html
        self.programs_dir = "../programs"
        self.repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            messagebox.showwarning(
                "Advertencia", 
                "Token de GitHub no encontrado. Configure GITHUB_TOKEN en las variables de entorno."
            )
        
        # Estilo
        style = ttk.Style()
        style.configure("Custom.TFrame", background='#2b2b2b')
        style.configure("Custom.TLabel", background='#2b2b2b', foreground='#ffffff')
        style.configure("Custom.TButton", padding=5)
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20", style="Custom.TFrame")
        main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        
        # Selector de programa
        program_frame = ttk.LabelFrame(main_frame, text="Selección de Programa", padding="10")
        program_frame.grid(row=0, column=0, columnspan=2, sticky=(W, E), pady=(0, 20))
        
        self.program_list = ttk.Combobox(program_frame, width=50)
        self.program_list.pack(fill=X)
        self.program_list.bind('<<ComboboxSelected>>', self.load_versions)
        
        # Frame izquierdo - Años y versiones existentes
        versions_frame = ttk.LabelFrame(main_frame, text="Versiones Existentes", padding="10")
        versions_frame.grid(row=1, column=0, sticky=(N, S, W, E), padx=(0, 10))
        
        self.versions_tree = ttk.Treeview(versions_frame, selectmode='extended')
        self.versions_tree.pack(fill=BOTH, expand=True)
        self.versions_tree['columns'] = ('year', 'version')
        self.versions_tree.column('#0', width=0, stretch=NO)
        self.versions_tree.column('year', width=100)
        self.versions_tree.column('version', width=150)
        self.versions_tree.heading('year', text='Año')
        self.versions_tree.heading('version', text='Versión')
        
        # Frame derecho - Agregar versiones
        add_frame = ttk.LabelFrame(main_frame, text="Agregar Nueva Versión", padding="10")
        add_frame.grid(row=1, column=1, sticky=(N, S, W, E))
        
        ttk.Label(add_frame, text="Año:").grid(row=0, column=0, sticky=W)
        self.year_entry = ttk.Entry(add_frame, width=10)
        self.year_entry.grid(row=0, column=1, sticky=W, pady=5)
        
        ttk.Label(add_frame, text="Versión:").grid(row=1, column=0, sticky=W)
        self.version_entry = ttk.Entry(add_frame, width=20)
        self.version_entry.grid(row=1, column=1, sticky=W, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Agregar Versión", 
                  command=self.add_version).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Seleccionados", 
                  command=self.delete_selected).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Guardar Cambios", 
                  command=self.save_changes).pack(side=LEFT, padx=5)
        
        # Cargar programas
        self.load_programs()
        
    def load_programs(self):
        """Cargar los archivos details.html disponibles"""
        details_files = []
        for file in os.listdir(self.programs_dir):
            if file.endswith("-details.html"):
                details_files.append(file)
        self.program_list['values'] = details_files
        if details_files:
            self.program_list.set(details_files[0])
            self.load_versions(None)

    def load_versions(self, event):
        """Cargar versiones existentes del programa seleccionado"""
        self.versions_tree.delete(*self.versions_tree.get_children())
        selected_file = self.program_list.get()
        if not selected_file:
            return
            
        file_path = os.path.join(self.programs_dir, selected_file)
        if not os.path.exists(file_path):
            return
            
        # Leer el archivo y extraer las versiones
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Buscar entre las etiquetas AÑOS-START y AÑOS-END
            pattern = r'<!-- AÑOS-START -->(.*?)<!-- AÑOS-END -->'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                versions_section = match.group(1)
                # Extraer años y versiones
                year_pattern = r'<li>(\d{4})'
                version_pattern = r'<span.*?>(.*?)</span>'
                years = re.findall(year_pattern, versions_section)
                versions = re.findall(version_pattern, versions_section)
                
                for i, (year, version) in enumerate(zip(years, versions)):
                    self.versions_tree.insert('', 'end', values=(year, version))

    def add_version(self):
        """Agregar nueva versión"""
        year = self.year_entry.get().strip()
        version = self.version_entry.get().strip()
        
        if not year or not version:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        if not year.isdigit() or len(year) != 4:
            messagebox.showerror("Error", "Por favor ingrese un año válido (4 dígitos)")
            return
            
        self.versions_tree.insert('', 'end', values=(year, version))
        self.year_entry.delete(0, END)
        self.version_entry.delete(0, END)

    def delete_selected(self):
        """Eliminar versiones seleccionadas"""
        selected_items = self.versions_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Por favor seleccione las versiones a eliminar")
            return
            
        for item in selected_items:
            self.versions_tree.delete(item)

    def sync_with_github(self, commit_message):
        """Sincronizar cambios con GitHub"""
        try:
            if not self.github_token:
                raise EnvironmentError("Token de GitHub no encontrado")

            repo_url = f"https://{self.github_token}@github.com/feede333/premiumdownloads3.git"
            
            # Ejecutar comandos git
            subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], 
                         cwd=self.repo_path, check=True)
            subprocess.run(['git', 'add', '.'], 
                         cwd=self.repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         cwd=self.repo_path, check=True)
            subprocess.run(['git', 'pull', 'origin', 'main', '--rebase'], 
                         cwd=self.repo_path, check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], 
                         cwd=self.repo_path, check=True)
            
            print("✅ Cambios sincronizados con GitHub")
            return True

        except Exception as e:
            error_msg = f"Error sincronizando con GitHub: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
            return False

    def save_changes(self):
        """Guardar cambios en el archivo y en GitHub"""
        selected_file = self.program_list.get()
        if not selected_file:
            return
            
        file_path = os.path.join(self.programs_dir, selected_file)
        
        # Construir la sección de versiones con el formato correcto
        versions_html = []
        for item in self.versions_tree.get_children():
            year, version = self.versions_tree.item(item)['values']
            versions_html.append(
                f'<li class="year-item">\n'
                f'                        <a href="#" class="year-link">\n'
                f'                            <span class="year">{year}</span>\n'
                f'                            <span class="version-count">{version}</span>\n'
                f'                            <i class="fas fa-chevron-right"></i>\n'
                f'                        </a>\n'
                f'                    </li>'
            )
        
        versions_section = "\n".join(versions_html)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Reemplazar la sección de versiones
        new_content = re.sub(
            r'(<!-- AÑOS-START -->).*?(<!-- AÑOS-END -->)',
            f'\\1\n                    {versions_section}\n                    \\2',
            content,
            flags=re.DOTALL
        )
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
            
        try:
            # Después de guardar los cambios localmente
            commit_msg = f"Updated versions for {selected_file}"
            if self.sync_with_github(commit_msg):
                messagebox.showinfo("Éxito", 
                    "Cambios guardados y sincronizados con GitHub correctamente")
            else:
                messagebox.showwarning("Advertencia", 
                    "Cambios guardados localmente pero no sincronizados con GitHub")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")

def main():
    root = Tk()
    app = VersionManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()