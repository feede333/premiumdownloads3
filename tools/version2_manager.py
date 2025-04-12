import os
from tkinter import *
from tkinter import ttk, messagebox
import re
import subprocess
import json
try:
    from git import Repo
except ImportError:
    messagebox.showerror("Error", "GitPython no está instalado. Por favor ejecute: pip install GitPython")
    raise

class VersionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Versiones")
        self.root.geometry("900x700")
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
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Selector de programa
        program_frame = ttk.LabelFrame(main_frame, text="Selección de Programa", padding="10")
        program_frame.grid(row=0, column=0, columnspan=2, sticky=(W, E), pady=(0, 20))
        
        self.program_list = ttk.Combobox(program_frame, width=50)
        self.program_list.pack(fill=X)
        self.program_list.bind('<<ComboboxSelected>>', self.load_versions)
        
        # Frame izquierdo - Años y versiones existentes
        versions_frame = ttk.LabelFrame(main_frame, text="Versiones Existentes", padding="10")
        versions_frame.grid(row=1, column=0, sticky=(N, S, W, E), padx=(0, 10))
        versions_frame.columnconfigure(0, weight=1)
        versions_frame.rowconfigure(0, weight=1)
        
        # Crear un frame con scrollbar para el treeview
        tree_frame = ttk.Frame(versions_frame)
        tree_frame.grid(row=0, column=0, sticky=(N, S, W, E))
        
        # Scrollbar vertical
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        
        # Scrollbar horizontal
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side='bottom', fill='x')
        
        self.versions_tree = ttk.Treeview(tree_frame, selectmode='extended',  # Cambiar 'browse' por 'extended'
                                         yscrollcommand=vsb.set,
                                         xscrollcommand=hsb.set)
        self.versions_tree.pack(fill=BOTH, expand=True)
        
        vsb.config(command=self.versions_tree.yview)
        hsb.config(command=self.versions_tree.xview)
        
        self.versions_tree['columns'] = ('year', 'version', 'date', 'size', 'torrentLink', 'magnetLink', 'seeds', 'peers')
        self.versions_tree.column('#0', width=0, stretch=NO)
        self.versions_tree.column('year', width=60, minwidth=50)
        self.versions_tree.column('version', width=120, minwidth=80)
        self.versions_tree.column('date', width=100, minwidth=80)
        self.versions_tree.column('size', width=80, minwidth=60)
        self.versions_tree.column('torrentLink', width=150, minwidth=100)
        self.versions_tree.column('magnetLink', width=150, minwidth=100)
        self.versions_tree.column('seeds', width=60, minwidth=50)
        self.versions_tree.column('peers', width=60, minwidth=50)
        
        self.versions_tree.heading('year', text='Año')
        self.versions_tree.heading('version', text='Versión')
        self.versions_tree.heading('date', text='Fecha')
        self.versions_tree.heading('size', text='Tamaño')
        self.versions_tree.heading('torrentLink', text='Link Torrent')
        self.versions_tree.heading('magnetLink', text='Link Magnet')
        self.versions_tree.heading('seeds', text='Seeds')
        self.versions_tree.heading('peers', text='Peers')
        
        self.versions_tree.bind("<Double-1>", self.edit_version)  # Solo mantener esta línea
        
        # Frame derecho - Agregar/Editar versiones
        self.add_frame = ttk.LabelFrame(main_frame, text="Gestionar Versión", padding="10")
        self.add_frame.grid(row=1, column=1, sticky=(N, S, W, E))
        
        # Grid para los campos de entrada
        row_count = 0
        ttk.Label(self.add_frame, text="Año:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.year_entry = ttk.Entry(self.add_frame, width=10)
        self.year_entry.grid(row=row_count, column=1, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Versión:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.version_entry = ttk.Entry(self.add_frame, width=20)
        self.version_entry.grid(row=row_count, column=1, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Fecha:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.date_entry = ttk.Entry(self.add_frame, width=20)
        self.date_entry.grid(row=row_count, column=1, sticky=W, pady=5)
        ttk.Label(self.add_frame, text="Ej: Abril 2023").grid(row=row_count, column=2, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Tamaño:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.size_entry = ttk.Entry(self.add_frame, width=15)
        self.size_entry.grid(row=row_count, column=1, sticky=W, pady=5)
        ttk.Label(self.add_frame, text="Ej: 4.2 GB").grid(row=row_count, column=2, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Link Torrent:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.torrent_entry = ttk.Entry(self.add_frame, width=40)
        self.torrent_entry.grid(row=row_count, column=1, columnspan=2, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Link Magnet:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.magnet_entry = ttk.Entry(self.add_frame, width=40)
        self.magnet_entry.grid(row=row_count, column=1, columnspan=2, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Seeds:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.seeds_entry = ttk.Entry(self.add_frame, width=10)
        self.seeds_entry.grid(row=row_count, column=1, sticky=W, pady=5)
        row_count += 1
        
        ttk.Label(self.add_frame, text="Peers:").grid(row=row_count, column=0, sticky=W, pady=5)
        self.peers_entry = ttk.Entry(self.add_frame, width=10)
        self.peers_entry.grid(row=row_count, column=1, sticky=W, pady=5)
        row_count += 1
        
        # Botones de acción para versiones
        version_btn_frame = ttk.Frame(self.add_frame)
        version_btn_frame.grid(row=row_count, column=0, columnspan=3, pady=10)
        
        self.edit_mode = False
        self.editing_item = None
        
        self.add_button = ttk.Button(version_btn_frame, text="Agregar Versión", 
                              command=self.add_version)
        self.add_button.pack(side=LEFT, padx=5)
        
        self.update_button = ttk.Button(version_btn_frame, text="Actualizar Versión", 
                                command=self.update_version, state=DISABLED)
        self.update_button.pack(side=LEFT, padx=5)
        
        ttk.Button(version_btn_frame, text="Cancelar Edición", 
                  command=self.cancel_edit).pack(side=LEFT, padx=5)
        
        # Botones de manejo general
        btn_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
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
        
        program_name = selected_file.replace('-details.html', '')
        subpages_dir = os.path.join(os.path.dirname(self.programs_dir), 'subpages')
        program_dir = os.path.join(subpages_dir, program_name)
        
        # Cargar solo desde los HTML si existen
        if (os.path.exists(program_dir)):
            for file in os.listdir(program_dir):
                if file.startswith(f"{program_name}-") and file.endswith(".html"):
                    year = file.replace(f"{program_name}-", "").replace(".html", "")
                    if year.isdigit() and len(year) == 4:
                        html_path = os.path.join(program_dir, file)
                        self.extract_versions_from_html(html_path, year)
        else:
            # Si no hay archivos HTML, cargar desde details.html
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                pattern = r'<!-- AÑOS-START -->(.*?)<!-- AÑOS-END -->'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    versions_section = match.group(1)
                    year_pattern = r'<li.*?>\s*<a.*?>\s*<span class="year">(\d{4})</span>\s*<span class="version-count">(.*?)</span>'
                    years_versions = re.findall(year_pattern, versions_section, re.DOTALL)
                    
                    for year, version in years_versions:
                        self.versions_tree.insert('', 'end', values=(
                            year, version, f"Abril {year}", "4.2 GB", 
                            "https://pasteplay.com/TUENLACE", 
                            "magnet:?xt=urn:btih:HASH", "50", "20"
                        ))
        
        # Limpiar los campos de entrada
        self.clear_entries()
        self.edit_mode = False
        self.editing_item = None

    def extract_versions_from_html(self, html_path, year):
        """Extraer información de versiones desde el archivo HTML del año"""
        with open(html_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Buscar el objeto JSON en el script
            script_pattern = r'const data = ({.*?});'
            script_match = re.search(script_pattern, content, re.DOTALL)
            
            if (script_match):
                try:
                    data_text = script_match.group(1)
                    data = json.loads(data_text)
                    
                    for version_data in data.get("versions", []):
                        self.versions_tree.insert('', 'end', values=(
                            year,
                            version_data.get("version", ""),
                            version_data.get("date", ""),
                            version_data.get("size", ""),
                            version_data.get("torrentLink", ""),
                            version_data.get("magnetLink", ""),
                            version_data.get("seeds", ""),
                            version_data.get("peers", "")
                        ))
                except json.JSONDecodeError:
                    # Si no se puede analizar el JSON, intentamos extraer los valores manualmente
                    version_pattern = r'"version": "(.*?)"'
                    date_pattern = r'"date": "(.*?)"'
                    size_pattern = r'"size": "(.*?)"'
                    torrent_pattern = r'"torrentLink": "(.*?)"'
                    magnet_pattern = r'"magnetLink": "(.*?)"'
                    seeds_pattern = r'"seeds": "(.*?)"'
                    peers_pattern = r'"peers": "(.*?)"'
                    
                    version = re.search(version_pattern, data_text)
                    date = re.search(date_pattern, data_text)
                    size = re.search(size_pattern, data_text)
                    torrent = re.search(torrent_pattern, data_text)
                    magnet = re.search(magnet_pattern, data_text)
                    seeds = re.search(seeds_pattern, data_text)
                    peers = re.search(peers_pattern, data_text)
                    
                    self.versions_tree.insert('', 'end', values=(
                        year,
                        version.group(1) if version else "",
                        date.group(1) if date else "",
                        size.group(1) if size else "",
                        torrent.group(1) if torrent else "",
                        magnet.group(1) if magnet else "",
                        seeds.group(1) if seeds else "",
                        peers.group(1) if peers else ""
                    ))

    def edit_version(self, event):
        """Editar una versión seleccionada"""
        selected = self.versions_tree.selection()
        if not selected:
            return
            
        # Obtener el item seleccionado
        item = selected[0]
        values = self.versions_tree.item(item)['values']
        
        # Llenar los campos
        entries = [self.year_entry, self.version_entry, self.date_entry, 
                  self.size_entry, self.torrent_entry, self.magnet_entry,
                  self.seeds_entry, self.peers_entry]
        
        for entry, value in zip(entries, values):
            entry.delete(0, END)
            entry.insert(0, value)
        
        # Activar modo edición
        self.edit_mode = True
        self.editing_item = item
        self.update_button.config(state=NORMAL)
        self.add_button.config(state=DISABLED)
        self.add_frame.config(text="Editar Versión")

    def clear_entries(self):
        """Limpia todos los campos de entrada"""
        self.year_entry.delete(0, END)
        self.version_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.size_entry.delete(0, END)
        self.torrent_entry.delete(0, END)
        self.magnet_entry.delete(0, END)
        self.seeds_entry.delete(0, END)
        self.peers_entry.delete(0, END)
        
        # Restaurar el texto del frame
        self.add_frame.config(text="Gestionar Versión")

    def cancel_edit(self):
        """Cancelar la edición actual"""
        self.clear_entries()
        self.edit_mode = False
        self.editing_item = None
        self.update_button.config(state=DISABLED)
        self.add_button.config(state=NORMAL)

    def get_entry_values(self):
        """Obtener los valores de los campos de entrada"""
        year = self.year_entry.get().strip()
        version = self.version_entry.get().strip()
        date = self.date_entry.get().strip()
        size = self.size_entry.get().strip()
        torrent_link = self.torrent_entry.get().strip()
        magnet_link = self.magnet_entry.get().strip()
        seeds = self.seeds_entry.get().strip()
        peers = self.peers_entry.get().strip()
        
        # Valores predeterminados
        if not date:
            date = f"Abril {year}"
        if not size:
            size = "4.2 GB"
        if not torrent_link:
            torrent_link = "https://pasteplay.com/TUENLACE"
        if not magnet_link:
            magnet_link = "magnet:?xt=urn:btih:HASH"
        if not seeds:
            seeds = "50"
        if not peers:
            peers = "20"
            
        return (year, version, date, size, torrent_link, magnet_link, seeds, peers)

    def add_version(self):
        """Agregar nueva versión"""
        year = self.year_entry.get().strip()
        version = self.version_entry.get().strip()
        
        if not year or not version:
            messagebox.showerror("Error", "Por favor complete al menos los campos de Año y Versión")
            return
            
        if not year.isdigit() or len(year) != 4:
            messagebox.showerror("Error", "Por favor ingrese un año válido (4 dígitos)")
            return
        
        # Permitir múltiples versiones por año
        values = self.get_entry_values()
        self.versions_tree.insert('', 'end', values=values)
        
        # Ordenar las versiones por año y mantener el orden de inserción dentro del mismo año
        items = [(self.versions_tree.item(item)["values"], item) for item in self.versions_tree.get_children('')]
        items.sort(key=lambda x: (x[0][0], self.versions_tree.index(x[1])))
        
        for idx, (_, item) in enumerate(items):
            self.versions_tree.move(item, '', idx)
        
        self.clear_entries()

    def update_version(self):
        """Actualizar una versión existente"""
        if not self.edit_mode or not self.editing_item:
            messagebox.showwarning("Advertencia", "No hay versión seleccionada para editar")
            return
            
        # Validaciones
        year = self.year_entry.get().strip()
        version = self.version_entry.get().strip()
        
        if not year or not version:
            messagebox.showerror("Error", "Por favor complete al menos los campos de Año y Versión")
            return
            
        if not year.isdigit() or len(year) != 4:
            messagebox.showerror("Error", "Por favor ingrese un año válido (4 dígitos)")
            return
        
        # Obtener valores actualizados
        values = self.get_entry_values()
        
        # Actualizar el item en el treeview
        self.versions_tree.item(self.editing_item, values=values)
        
        # Limpiar y resetear
        self.clear_entries()
        self.edit_mode = False
        self.editing_item = None
        self.update_button.config(state=DISABLED)
        self.add_button.config(state=NORMAL)
        
        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Versión actualizada correctamente")

    def delete_selected(self):
        """Eliminar versiones seleccionadas"""
        selected_items = self.versions_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Por favor seleccione las versiones a eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar las versiones seleccionadas?"):
            selected_file = self.program_list.get()
            program_name = selected_file.replace('-details.html', '')
            subpages_dir = os.path.join(os.path.dirname(self.programs_dir), 'subpages')
            program_dir = os.path.join(subpages_dir, program_name)
            
            years_to_delete = set()
            for item in selected_items:
                values = self.versions_tree.item(item)['values']
                year = values[0]
                years_to_delete.add(year)
                self.versions_tree.delete(item)
            
            # Eliminar archivos HTML correspondientes
            for year in years_to_delete:
                html_file = f"{program_name}-{year}.html"
                file_path = os.path.join(program_dir, html_file)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo eliminar el archivo {html_file}: {str(e)}")
            
            # Verificar si la carpeta del programa quedó vacía
            if os.path.exists(program_dir) and not os.listdir(program_dir):
                try:
                    os.rmdir(program_dir)
                except Exception as e:
                    print(f"No se pudo eliminar la carpeta vacía: {str(e)}")

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
        program_name = selected_file.replace('-details.html', '')
        
        # Crear directorio en subpages
        subpages_dir = os.path.join(os.path.dirname(self.programs_dir), 'subpages')
        program_dir = os.path.join(subpages_dir, program_name)
        if not os.path.exists(program_dir):
            os.makedirs(program_dir)
        
        # Agrupar versiones por año
        years_data = {}
        for item in self.versions_tree.get_children():
            values = self.versions_tree.item(item)['values']
            year = values[0]
            
            if year not in years_data:
                years_data[year] = []
                
            years_data[year].append({
                "version": values[1],
                "date": values[2],
                "size": values[3],
                "torrentLink": values[4],
                "magnetLink": values[5],
                "seeds": values[6],
                "peers": values[7]
            })
        
        # Construir la sección de versiones y crear archivos HTML por año
        versions_html = []
        for year, versions in years_data.items():
            # Crear archivo HTML para el año
            year_file = f"{program_name}-{year}.html"
            year_path = os.path.join(program_dir, year_file)
            
            # Crear JSON de versiones para este año
            versions_json = json.dumps({"versions": versions}, indent=4)
            
            script_section = """
            <script>
            document.addEventListener('DOMContentLoaded', () => {
                const data = %s;

                const versionList = document.querySelector('.version-list');
                versionList.innerHTML = data.versions.map(version => `
                    <div class="version-item">
                        <div class="version-info">
                            <h3 class="version-name">${version.version}</h3>
                            <span class="version-date">${version.date}</span>
                            <span class="file-size">${version.size}</span>
                        </div>
                        <div class="download-container">
                            <div class="download-options">
                                <a href="${version.magnetLink}" class="magnet-button">
                                    <i class="fas fa-magnet"></i>
                                    <span>Magnet</span>
                                </a>
                                <a href="${version.torrentLink}" class="torrent-button" target="_blank">
                                    <i class="fas fa-download"></i>
                                    <span>Torrent</span>
                                </a>
                            </div>
                            <div class="torrent-stats">
                                <div class="peer-info">
                                    <span class="seeds-indicator"></span>
                                    <span>Seeds: ${version.seeds}</span>
                                </div>
                                <div class="peer-info">
                                    <span class="peers-indicator"></span>
                                    <span>Peers: ${version.peers}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            });
            </script>
            """ % versions_json

            year_template = f"""<!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{program_name} {year} - Versiones</title>
                <link rel="stylesheet" href="../csscomun.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
                <script src="../js/torrentTrackerversiones.js"></script>
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
                    <a href="../{selected_file.replace('-details.html', '.html')}" class="back-link">
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
                        <p>© {year} PremiumDownloads. Todos los derechos reservados.</p>
                    </div>
                </footer>

                {script_section}
            </body>
            </html>"""

            with open(year_path, 'w', encoding='utf-8') as year_file:
                year_file.write(year_template)
            
            # Actualizar el HTML con el enlace correcto y la versión
            # Para details.html solo mostramos el año y la versión más reciente
            if versions:
                latest_version = versions[0]['version']
                versions_html.append(
                    f'<li class="year-item">\n'
                    f'                        <a href="../subpages/{program_name}/{program_name}-{year}.html" class="year-link">\n'
                    f'                            <span class="year">{year}</span>\n'
                    f'                            <span class="version-count">{latest_version}</span>\n'
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