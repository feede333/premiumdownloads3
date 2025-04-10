import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import shutil
from datetime import datetime

class VersionManager:
    def __init__(self):
        self.base_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2"
        self.programs_path = os.path.join(self.base_path, "programs")
        self.subpages_path = os.path.join(self.base_path, "subpages")
        self.css_path = os.path.join(self.base_path, "css")
        
        # Crear directorios base si no existen
        os.makedirs(self.programs_path, exist_ok=True)
        os.makedirs(self.subpages_path, exist_ok=True)
        os.makedirs(self.css_path, exist_ok=True)

        # No es necesario copiar el csscomun.css ya que debe permanecer en subpages

        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise EnvironmentError("GITHUB_TOKEN environment variable not found")
        
        # Inicializar repositorio Git si no existe
        if not os.path.exists(os.path.join(self.base_path, ".git")):
            try:
                subprocess.run(['git', 'init'], cwd=self.base_path, check=True)
                subprocess.run(['git', 'config', '--global', 'user.name', 'feede333'], cwd=self.base_path, check=True)
                subprocess.run(['git', 'config', '--global', 'user.email', 'your.email@example.com'], cwd=self.base_path, check=True)
                print("✅ Repositorio Git inicializado")
            except Exception as e:
                print(f"❌ Error inicializando Git: {str(e)}")

    def validate_program_name(self, program_name):
        """Valida que el nombre del programa no tenga caracteres especiales"""
        import re
        if not program_name or not program_name.strip():
            messagebox.showerror("Error", "El nombre del programa no puede estar vacío")
            return False
        
        if not re.match("^[a-zA-Z0-9\\s-]+$", program_name):
            messagebox.showerror("Error", "El nombre del programa solo puede contener letras, números, espacios y guiones")
            return False
        return True

    def create_program_structure(self, program_name):
        try:
            # Validar nombre del programa
            if not self.validate_program_name(program_name):
                return False

            # Normalizar el nombre del programa para usarlo en rutas
            program_id = program_name.lower().replace(' ', '-')
            
            # 1. Crear carpeta específica del programa en subpages
            program_subpages = os.path.join(self.subpages_path, program_id)
            os.makedirs(program_subpages, exist_ok=True)
            
            # Copiar csscomun.css al directorio del programa
            css_src = os.path.join(self.subpages_path, "csscomun.css")
            css_dest = os.path.join(program_subpages, "csscomun.css")
            if os.path.exists(css_src):
                shutil.copy2(css_src, css_dest)
                print(f"✅ CSS común copiado: {css_dest}")

            # 2. Crear archivo details específico del programa
            details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
            self.create_details_file(program_name, program_id)
            
            print(f"\n✅ Estructura creada para {program_name}:")
            print(f"  📁 Carpeta: {program_subpages}")
            print(f"  📄 Details: {details_path}")
            print(f"  📄 CSS: {css_dest}\n")
            
            # Actualizar index.html y sincronizar
            self.update_index_page()
            self.sync_with_github(f"Add: Nuevo programa {program_name}")
            return program_id
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la estructura: {str(e)}")
            return False

    def create_details_file(self, program_name, program_id):
        """Crea el archivo details.html específico para el programa"""
        details_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{program_name} - Detalles | PremiumDownloads</title>
    <link rel="stylesheet" href="../css/detail.css">  <!-- Ruta corregida para detail.css -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
    <header>
        <div class="container header-content">
            <a href="../index.html" class="logo">
                <span>⬇️</span>
                <span>PremiumDownloads</span>
            </a>
            <nav>
                <ul>
                    <li><a href="../index.html">Inicio</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        <div class="download-versions">
            <h3 class="versions-title">Versiones de {program_name}</h3>
            <ul class="version-years">
                <!-- AÑOS-START -->
                <!-- Las versiones se insertarán aquí -->
                <!-- AÑOS-END -->
            </ul>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="#">Términos de uso</a>
                <a href="#">Política de privacidad</a>
                <a href="#">DMCA</a>
                <a href="#">Contacto</a>
            </div>
            <p>© {datetime.now().year} PremiumDownloads. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>"""

        details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
        with open(details_path, "w", encoding="utf-8") as file:
            file.write(details_content)

    def create_html_file(self, program_name, year):
        try:
            program_id = program_name.lower().replace(' ', '-')
            program_path = os.path.join(self.subpages_path, program_id)
            file_name = f"{year}.html"
            file_path = os.path.join(program_path, file_name)

            # Crear archivo HTML con referencia al csscomun.css
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{program_name} {year} - Versiones</title>
    <link rel="stylesheet" href="../csscomun.css">  <!-- Ruta corregida para csscomun.css -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
    <header>
        <div class="container header-content">
            <a href="../../index.html" class="logo">
                <span>⬇️</span>
                <span>PremiumDownloads</span>
            </a>
            <nav>
                <ul>
                    <li><a href="../../index.html">Inicio</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        <a href="../../programs/{program_id}-details.html" class="back-link">
            <i class="fa fa-arrow-left"></i> Volver a detalles
        </a>

        <div class="download-detail">
            <h2>Versiones de {year}</h2>
            
            <div class="version-list">
                <!-- Las versiones se cargarán dinámicamente -->
            </div>

            <div class="torrent-note">
                <p><i class="fas fa-info-circle"></i> Para usar estos enlaces necesitas:</p>
                <ul>
                    <li>• qBittorrent (Recomendado)</li>
                    <li>• uTorrent</li>
                    <li>• BitTorrent</li>
                </ul>
            </div>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="#">Términos de uso</a>
                <a href="#">Política de privacidad</a>
                <a href="#">DMCA</a>
                <a href="#">Contacto</a>
            </div>
            <p>© {datetime.now().year} PremiumDownloads. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>""")

            return True

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear archivo: {str(e)}")
            return False

    def list_html_files(self, program_id):
        program_path = os.path.join(self.subpages_path, program_id)
        files = [f for f in os.listdir(program_path) if f.endswith(".html")]
        return files

    def read_versions_from_html(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                
            # Buscar el array de versiones en el contenido
            start = content.find('"versions": [') + len('"versions": [')
            end = content.find(']', start)
            versions_json = content[start:end].strip()
            
            if not versions_json:
                return []  # Retorna lista vacía si no hay versiones
                
            try:
                return json.loads(f"[{versions_json}]")
            except json.JSONDecodeError:
                return []  # Retorna lista vacía si hay error al decodificar JSON
                
        except Exception as e:
            # Solo mostrar error si no es un archivo recién creado
            if os.path.getsize(file_path) > 0:
                messagebox.showerror("Error", f"Error al leer las versiones: {str(e)}")
            return []

    def save_versions_to_html(self, file_path, versions):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            start = content.find('"versions": [') + len('"versions": [')
            end = content.find(']', start)
            
            new_content = (
                content[:start] + 
                "\n    " + 
                json.dumps(versions, indent=4)[1:-1] + 
                "\n" + 
                content[end:]
            )
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar las versiones: {str(e)}")
            return False

    def delete_html_file(self, file_path, filename):
        try:
            os.remove(file_path)
            # Actualizar el archivo details del programa después de eliminar
            program_id = filename.split('-')[0]
            self.update_program_details(program_id)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el archivo: {str(e)}")
            return False

    def delete_program(self, program_id):
        """Elimina un programa completo (carpeta y details)"""
        try:
            # Eliminar carpeta en subpages
            program_path = os.path.join(self.subpages_path, program_id)
            if os.path.exists(program_path):
                import shutil
                shutil.rmtree(program_path)

            # Eliminar archivo details
            details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
            if os.path.exists(details_path):
                os.remove(details_path)

            # Actualizar index.html
            self.update_index_page()
            
            # Sincronizar con GitHub
            self.sync_with_github(f"Remove: Programa {program_id}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el programa: {str(e)}")
            return False

    def update_program_details(self, program_id):
        """Actualiza el archivo details.html del programa con los enlaces a los archivos de años disponibles"""
        details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
        program_path = os.path.join(self.subpages_path, program_id)
        
        try:
            # Obtener lista de años ordenados de manera descendente
            years = sorted([f.replace('.html', '') for f in os.listdir(program_path) 
                           if f.endswith('.html')], key=int, reverse=True)
            
            # Leer el contenido actual del archivo details.html
            with open(details_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {details_path}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo details: {str(e)}")
            return False

        try:
                
            # Encontrar la sección donde se insertan los años
            start_marker = '<!-- AÑOS-START -->'
            end_marker = '<!-- AÑOS-END -->'
            start = content.find(start_marker)
            end = content.find(end_marker)
            
            if start == -1 or end == -1:
                messagebox.showerror("Error", "No se encontraron los marcadores en el archivo details.html")
                return False
            
            # Generar el nuevo contenido HTML para los años
            years_html = []
            for year in years:
                # Contar versiones para este año
                file_path = os.path.join(program_path, f"{year}.html")
                versions = self.read_versions_from_html(file_path)
                version_count = len(versions)
                
                years_html.append(f'''
                            <li class="year-item">
                                <a href="./{program_id}/{year}.html" class="year-link">
                                    <span class="year">{year}</span>
                                    <span class="version-count">({version_count} versiones)</span>
                                    <i class="fas fa-chevron-right"></i>
                                </a>
                            </li>''')
            
            # Insertar el nuevo contenido
            new_content = (
                content[:start + len(start_marker)] + 
                '\n' + 
                ''.join(years_html) + 
                '\n                        ' +
                content[end:]
            )
            
            # Guardar los cambios
            with open(details_path, "w", encoding="utf-8") as file:
                file.write(new_content)
                
            return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el archivo details.html: {str(e)}")
            return False

    def log_change(self, action, details):
        """Registra cambios en un archivo de log"""
        log_path = os.path.join(self.base_path, "changes.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] {action}: {details}\n")

    def sync_with_github(self, commit_message):
        """Sincroniza los cambios con GitHub"""
        try:
            if not self.token:
                raise EnvironmentError("Token de GitHub no encontrado")

            # Inicializar Git si no existe
            if not os.path.exists(os.path.join(self.base_path, ".git")):
                print("Inicializando repositorio Git...")
                subprocess.run(['git', 'init'], cwd=self.base_path, check=True)
                subprocess.run(['git', 'config', '--global', 'user.name', 'feede333'], cwd=self.base_path, check=True)
                subprocess.run(['git', 'config', '--global', 'user.email', 'your.email@example.com'], cwd=self.base_path, check=True)
                
                # Configurar remote
                repo_url = f"https://{self.token}@github.com/feede333/premiumdownloads3.git"
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], cwd=self.base_path, check=True)
                
                # Primera sincronización
                subprocess.run(['git', 'fetch'], cwd=self.base_path, check=True)
                subprocess.run(['git', 'checkout', '-b', 'main'], cwd=self.base_path, check=True)
            
            # Actualizar URL del remote (por si cambió el token)
            repo_url = f"https://{self.token}@github.com/feede333/premiumdownloads3.git"
            subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], cwd=self.base_path, check=True)
            
            # Sincronizar cambios
            print("\nSubiendo cambios a GitHub...")
            subprocess.run(['git', 'add', '.'], cwd=self.base_path, check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.base_path, check=True)
            subprocess.run(['git', 'pull', 'origin', 'main', '--rebase'], cwd=self.base_path, check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.base_path, check=True)
            
            print("✅ Cambios sincronizados con GitHub")
            return True

        except Exception as e:
            print(f"❌ Error sincronizando con GitHub: {str(e)}")
            messagebox.showerror("Error", f"Error sincronizando con GitHub: {str(e)}")
            return False

    def update_index_page(self):
        """Actualiza el index.html con los programas y sus enlaces"""
        try:
            index_path = os.path.join(self.base_path, "index.html")
            
            # Leer el contenido actual del index.html
            with open(index_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Encontrar la sección donde se insertan los programas
            start_marker = '<!-- PROGRAMS-START -->'
            end_marker = '<!-- PROGRAMS-END -->'
            start = content.find(start_marker)
            end = content.find(end_marker)

            if start == -1 or end == -1:
                raise ValueError("No se encontraron los marcadores en index.html")

            # Generar HTML para cada programa
            programs_html = []
            for program in self.get_programs():
                programs_html.append(f"""
                    <div class="program-card">
                        <h3>{program['name']}</h3>
                        <div class="program-meta">
                            <span>Versiones: {program['version_count']}</span>
                            <span>Última: {program['latest_year']}</span>
                        </div>
                        <a href="programs/{program['id']}-details.html" class="program-link">
                            Ver versiones <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                """)

            # Insertar el nuevo contenido
            new_content = (
                content[:start + len(start_marker)] +
                '\n' +
                ''.join(programs_html) +
                '\n' +
                content[end:]
            )

            # Guardar cambios
            with open(index_path, "w", encoding="utf-8") as file:
                file.write(new_content)

            print("✅ Index.html actualizado correctamente")
            return True

        except Exception as e:
            print(f"❌ Error actualizando index.html: {str(e)}")
            return False

class VersionManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Versiones")
        self.root.geometry("800x600")
        
        self.manager = VersionManager()
        
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = ttk.Label(self.root, text="Gestor de Versiones", style='Header.TLabel')
        header.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Button(main_frame, text="Crear Nuevo Programa", 
                  command=self.show_create_program_dialog).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Seleccionar Programa Existente", 
                  command=self.show_select_program_dialog).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Salir", 
                  command=self.root.quit).pack(fill='x', pady=5)

    def show_create_program_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nuevo Programa")
        dialog.geometry("400x200")
        dialog.grab_set()

        ttk.Label(dialog, text="Ingresa el nombre del programa:").pack(pady=20)
        program_entry = ttk.Entry(dialog)
        program_entry.pack(pady=5)

        def create_program():
            program_name = program_entry.get()
            if not self.manager.validate_program_name(program_name):
                return
            program_id = self.manager.create_program_structure(program_name)
            messagebox.showinfo("Éxito", f"Programa {program_name} creado correctamente.")
            dialog.destroy()
            self.show_program_management(program_id)

        ttk.Button(dialog, text="Crear", command=create_program).pack(pady=20)

    def show_select_program_dialog(self):
        programs = [f.replace('-details.html', '') for f in os.listdir(self.manager.programs_path) if f.endswith("-details.html")]
        if not programs:
            messagebox.showwarning("Aviso", "No se encontraron programas.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccionar Programa Existente")
        dialog.geometry("500x400")
        dialog.grab_set()

        ttk.Label(dialog, text="Selecciona los programas:", style='Header.TLabel').pack(pady=10)
        
        # Frame con scroll para la lista
        frame = ttk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox con selección múltiple
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode='multiple')
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=listbox.yview)
        
        # Cargar programas ordenados
        for program in sorted(programs):
            listbox.insert('end', program)

        # Frame para botones
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill='x', padx=10, pady=10)

        def manage_selected():
            if not listbox.curselection():
                messagebox.showwarning("Aviso", "Por favor selecciona un programa.")
                return
            program_id = listbox.get(listbox.curselection()[0])
            dialog.destroy()
            self.show_program_management(program_id)

        def delete_selected():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Aviso", "Por favor selecciona al menos un programa.")
                return
            
            selected_programs = [listbox.get(i) for i in selected_indices]
            if messagebox.askyesno("Confirmar eliminación", 
                                 f"¿Estás seguro que deseas eliminar los siguientes programas?\n\n" +
                                 "\n".join(f"- {p}" for p in selected_programs)):
                
                for program_id in selected_programs:
                    if self.manager.delete_program(program_id):
                        print(f"✅ Programa eliminado: {program_id}")
                
                dialog.destroy()
                messagebox.showinfo("Éxito", "Programas eliminados correctamente")
                self.show_select_program_dialog()  # Recargar diálogo

        def select_all():
            listbox.select_set(0, tk.END)

        def deselect_all():
            listbox.selection_clear(0, tk.END)

        # Botones de acción
        ttk.Button(button_frame, text="Gestionar Seleccionado", 
                  command=manage_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar Seleccionados", 
                  command=delete_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Seleccionar Todos", 
                  command=select_all).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Deseleccionar Todos", 
                  command=deselect_all).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cerrar", 
                  command=dialog.destroy).pack(side='right', padx=5)

    def show_program_management(self, program_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = ttk.Label(self.root, text=f"Gestión de Programa - {program_id}", 
                          style='Header.TLabel')
        header.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Button(main_frame, text="Agregar Año", 
                  command=lambda: self.show_add_year_dialog(program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Eliminar Año", 
                  command=lambda: self.show_remove_year_dialog(program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Listar Años", 
                  command=lambda: self.show_list_years(program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Vista Previa Details", 
                  command=lambda: self.show_details_preview(program_id.replace('-', ' ').title(), program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Eliminar Programa", 
                  command=lambda: self.delete_program_dialog(program_id)).pack(fill='x', pady=5)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Button(main_frame, text="Volver al menú principal", 
                  command=self.create_main_menu).pack(fill='x', pady=5)

    def show_add_year_dialog(self, program_id):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nuevo Año")
        dialog.geometry("400x200")
        dialog.grab_set()

        ttk.Label(dialog, text="Ingresa el año para el nuevo archivo:").pack(pady=20)
        year_entry = ttk.Entry(dialog)
        year_entry.pack(pady=5)

        def add_year():
            year = year_entry.get()
            program_name = program_id.replace('-', ' ').title()
            if self.manager.create_html_file(program_name, year):
                messagebox.showinfo("Éxito", f"Año {year} agregado correctamente.")
                dialog.destroy()

        ttk.Button(dialog, text="Agregar", command=add_year).pack(pady=20)

    def show_remove_year_dialog(self, program_id):
        years = self.manager.list_html_files(program_id)
        if not years:
            messagebox.showinfo("Info", "No hay años disponibles para eliminar")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Eliminar Año")
        dialog.geometry("400x300")
        dialog.grab_set()

        ttk.Label(dialog, text=f"Años de {program_id}:", style='Header.TLabel').pack(pady=10)
        
        # Frame con scroll para la lista
        frame = ttk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=listbox.yview)
        
        for year in sorted(years, key=lambda x: x.replace('.html', ''), reverse=True):
            listbox.insert('end', year.replace('.html', ''))
        
        def remove_year():
            if not listbox.curselection():
                messagebox.showwarning("Aviso", "Por favor selecciona un año.")
                return
                
            year = listbox.get(listbox.curselection()[0])
            file_path = os.path.join(self.manager.subpages_path, program_id, f"{year}.html")
            if self.manager.delete_html_file(file_path, f"{program_id}-{year}.html"):
                messagebox.showinfo("Éxito", f"Año {year} eliminado correctamente.")
                dialog.destroy()

        ttk.Button(dialog, text="Eliminar", command=remove_year).pack(pady=10)
        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def show_list_years(self, program_id):
        """Muestra una lista de años disponibles para el programa"""
        years = self.manager.list_html_files(program_id)
        if not years:
            messagebox.showinfo("Info", "No hay años disponibles")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Años Disponibles")
        dialog.geometry("400x300")
        dialog.grab_set()

        ttk.Label(dialog, text=f"Años de {program_id}:", style='Header.TLabel').pack(pady=10)
        
        # Frame con scroll para la lista
        frame = ttk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=listbox.yview)
        
        for year in sorted(years, key=lambda x: x.replace('.html', ''), reverse=True):
            listbox.insert('end', year.replace('.html', ''))
        
        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def show_details_preview(self, program_name, program_id):
        """Muestra una vista previa del archivo details"""
        details_path = os.path.join(self.manager.programs_path, f"{program_id}-details.html")
        
        try:
            with open(details_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")
            return

        preview = tk.Toplevel(self.root)
        preview.title(f"Vista Previa - {program_name}")
        preview.geometry("800x600")

        # Frame con scroll
        frame = ttk.Frame(preview)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=text.yview)
        
        text.insert('1.0', content)
        text.config(state='disabled')

        ttk.Button(preview, text="Cerrar", command=preview.destroy).pack(pady=10)

    def delete_program_dialog(self, program_id):
        """Diálogo para confirmar eliminación de programa"""
        if messagebox.askyesno("Confirmar eliminación", 
                             f"¿Estás seguro que deseas eliminar el programa {program_id}?\n\n" +
                             "Esta acción eliminará:\n" +
                             f"- La carpeta en subpages/{program_id}\n" +
                             f"- El archivo {program_id}-details.html\n\n" +
                             "Esta acción no se puede deshacer."):
            
            if self.manager.delete_program(program_id):
                messagebox.showinfo("Éxito", "Programa eliminado correctamente")
                self.create_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = VersionManagerGUI(root)
    root.mainloop()