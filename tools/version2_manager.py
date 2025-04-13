import os
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
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
        self.root.geometry("1024x768")
        
        # Directorio donde están los archivos details.html
        self.programs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "programs")
        self.repo_path = os.path.dirname(os.path.dirname(__file__))
        self.github_token = os.getenv("GITHUB_TOKEN")
        
        if not self.github_token:
            messagebox.showwarning(
                "Advertencia", 
                "Token de GitHub no encontrado. Configure GITHUB_TOKEN en las variables de entorno."
            )
        
        # Aplicar tema oscuro personalizado
        style = ttk.Style(theme="darkly")
        
        # Personalizar colores principales
        style.configure(
            "TLabel",
            foreground="#ffffff",
            background="#1e1e1e"
        )
        
        style.configure(
            "TFrame",
            background="#1e1e1e"
        )
        
        style.configure(
            "TLabelframe",
            background="#1e1e1e",
            foreground="#ffffff",
            bordercolor="#3d3d3d"
        )
        
        style.configure(
            "TLabelframe.Label",
            foreground="#ffffff",
            background="#1e1e1e",
            font=("Segoe UI", 10, "bold")
        )
        
        # Mejorar Treeview
        style.configure(
            "Treeview",
            background="#2d2d2d",
            foreground="#ffffff",
            fieldbackground="#2d2d2d",
            borderwidth=0,
            font=("Segoe UI", 9),
            rowheight=25
        )
        
        style.configure(
            "Treeview.Heading",
            background="#0d47a1",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=5
        )
        
        style.map(
            "Treeview.Heading",
            background=[("active", "#1565c0")]
        )
        
        # Mejorar botones
        style.configure(
            "primary.TButton",
            font=("Segoe UI", 9),
            padding=10
        )
        
        style.configure(
            "success.Outline.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=10
        )
        
        style.configure(
            "danger.Outline.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=10
        )
        
        # Frame principal con padding y bordes redondeados
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        
        # Barra de título personalizada
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(W, E), pady=(0, 20))
        
        logo_label = ttk.Label(
            title_frame,
            text="⬇️",
            font=("Segoe UI Emoji", 32)
        )
        logo_label.pack(side=LEFT, padx=(0, 10))
        
        ttk.Label(
            title_frame, 
            text="PremiumDownloads Manager", 
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-primary"
        ).pack(side=LEFT)

        # Selector de programa mejorado
        program_frame = ttk.LabelFrame(
            main_frame, 
            text="Selección de Programa",
            padding="10",
            bootstyle="primary"
        )
        program_frame.grid(row=0, column=0, columnspan=2, sticky=(W, E), pady=(0, 20))
        
        self.program_list = ttk.Combobox(program_frame, width=50)
        self.program_list.pack(fill=X)
        self.program_list.bind('<<ComboboxSelected>>', self.load_versions)
        
        # Barra de búsqueda mejorada
        search_frame = ttk.Frame(program_frame, style="Custom.TFrame")
        search_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(
            search_frame, 
            text="🔍",
            font=("Segoe UI Emoji", 14),
            foreground="#64b5f6"
        ).pack(side=LEFT, padx=5)
        
        self.search_entry = ttk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.search_entry.pack(side=LEFT, padx=5, fill=X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.search_versions)
        
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
        
        # TreeView mejorado
        self.versions_tree = ttk.Treeview(
            tree_frame, 
            selectmode='extended',
            bootstyle="primary",
            height=15
        )
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
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame, 
            text="✨ Agregar Versión",
            bootstyle="success-outline",
            command=self.add_version
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="🗑️ Eliminar Seleccionados",
            bootstyle="danger-outline",
            command=self.delete_selected
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="💾 Guardar Cambios",
            bootstyle="info-outline",
            command=self.save_changes
        ).pack(side=LEFT, padx=5)
        
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
                if (match):
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
            
            # Agregar cambios
            subprocess.run(['git', 'add', '.'], 
                         cwd=self.repo_path, check=True)
            
            # Verificar si hay cambios para commitear
            status = subprocess.run(['git', 'status', '--porcelain'],
                                  cwd=self.repo_path,
                                  capture_output=True,
                                  text=True)
            
            if not status.stdout.strip():
                print("✅ No hay cambios para sincronizar")
                return True
                
            # Si hay cambios, continuar con commit y push
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
                    <a href="../programs/{selected_file}" class="back-link">
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

    def edit_year_versions(self):
        """Abrir ventana de edición de versiones para el año seleccionado"""
        selected = self.versions_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Por favor seleccione un año para editar sus versiones")
            return

        item = selected[0]
        values = self.versions_tree.item(item)['values']
        year = values[0]

        # Crear ventana de edición
        edit_window = Toplevel(self.root)
        edit_window.title(f"Editar versiones del año {year}")
        edit_window.geometry("800x600")
        edit_window.configure(bg='#2b2b2b')

        # Frame principal
        main_frame = ttk.Frame(edit_window, padding="20", style="Custom.TFrame")
        main_frame.pack(fill=BOTH, expand=True)

        # Lista de versiones
        versions_frame = ttk.LabelFrame(main_frame, text=f"Versiones del año {year}", padding="10")
        versions_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Treeview para versiones
        tree_frame = ttk.Frame(versions_frame)
        tree_frame.pack(fill=BOTH, expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        versions_tree = ttk.Treeview(tree_frame, selectmode='browse',
                                    yscrollcommand=vsb.set,
                                    xscrollcommand=hsb.set)
        
        vsb.config(command=versions_tree.yview)
        hsb.config(command=versions_tree.xview)
        
        vsb.pack(side=RIGHT, fill=Y)
        hsb.pack(side=BOTTOM, fill=X)
        versions_tree.pack(fill=BOTH, expand=True)

        versions_tree['columns'] = ('version', 'date', 'size', 'torrent', 'magnet', 'seeds', 'peers')
        versions_tree.column('#0', width=0, stretch=NO)
        for col, width in zip(versions_tree['columns'], [120, 100, 80, 150, 150, 60, 60]):
            versions_tree.column(col, width=width, minwidth=50)
            versions_tree.heading(col, text=col.capitalize())

        # Frame para entrada de datos
        entry_frame = ttk.LabelFrame(main_frame, text="Nueva versión", padding="10")
        entry_frame.pack(fill=X, padx=5, pady=5)

        # Campos de entrada
        entries = {}
        row = 0
        for field in ['version', 'date', 'size', 'torrent', 'magnet', 'seeds', 'peers']:
            ttk.Label(entry_frame, text=f"{field.capitalize()}:").grid(row=row, column=0, sticky=W, pady=2)
            entries[field] = ttk.Entry(entry_frame, width=40)
            entries[field].grid(row=row, column=1, sticky=W, pady=2, padx=5)
            row += 1

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)

        def add_version():
            """Agregar nueva versión a la lista"""
            values = [entries[field].get().strip() for field in ['version', 'date', 'size', 'torrent', 'magnet', 'seeds', 'peers']]
            if not values[0]:  # Verificar al menos la versión
                messagebox.showerror("Error", "Por favor ingrese al menos la versión")
                return
            versions_tree.insert('', 'end', values=values)
            for entry in entries.values():
                entry.delete(0, END)

        def save_versions():
            """Guardar las versiones y actualizar el árbol principal"""
            versions = []
            for tree_item in versions_tree.get_children():
                values = versions_tree.item(tree_item)['values']
                versions.append({
                    "version": values[0],
                    "date": values[1] or f"Abril {year}",
                    "size": values[2] or "4.2 GB",
                    "torrentLink": values[3] or "https://pasteplay.com/TUENLACE",
                    "magnetLink": values[4] or "magnet:?xt=urn:btih:HASH",
                    "seeds": values[5] or "50",
                    "peers": values[6] or "20"
                })
            
            if versions:
                # Actualizar el item original en el árbol principal
                original_item = item  # Este es el item original que recibimos al abrir la ventana
                self.versions_tree.item(original_item, values=(
                    year, 
                    versions[0]["version"],  # Mostramos la primera versión en el árbol principal 
                    versions[0]["date"], 
                    versions[0]["size"],
                    versions[0]["torrentLink"], 
                    versions[0]["magnetLink"],
                    versions[0]["seeds"], 
                    versions[0]["peers"]
                ))
                
                # Guardar todas las versiones en el archivo HTML
                self.save_year_versions(year, versions)
                
                edit_window.destroy()
                messagebox.showinfo("Éxito", "Versiones guardadas correctamente")
                
                # Recargar las versiones para actualizar la vista
                self.load_versions(None)

        # Agregar binding para doble clic en una versión
        versions_tree.bind("<Double-1>", lambda e: edit_selected_version())
        
        # Variables para modo edición
        edit_mode = False
        editing_item = None
        
        def edit_selected_version():
            """Editar la versión seleccionada"""
            nonlocal edit_mode, editing_item
            selected = versions_tree.selection()
            if not selected:
                return
                
            # Obtener valores de la versión seleccionada
            item = selected[0]
            values = versions_tree.item(item)['values']
            
            # Llenar los campos con los valores actuales
            for field, value in zip(['version', 'date', 'size', 'torrent', 'magnet', 'seeds', 'peers'], values):
                entries[field].delete(0, END)
                entries[field].insert(0, value)
            
            # Activar modo edición
            edit_mode = True
            editing_item = item
            add_version_btn.config(state=DISABLED)
            update_version_btn.config(state=NORMAL)
            entry_frame.config(text="Editar versión")

        def cancel_edit():
            """Cancelar la edición actual"""
            nonlocal edit_mode, editing_item
            # Limpiar campos
            for entry in entries.values():
                entry.delete(0, END)
            
            # Resetear modo edición
            edit_mode = False
            editing_item = None
            add_version_btn.config(state=NORMAL)
            update_version_btn.config(state=DISABLED)
            entry_frame.config(text="Nueva versión")

        def add_version():
            """Agregar nueva versión a la lista"""
            values = [entries[field].get().strip() for field in ['version', 'date', 'size', 'torrent', 'magnet', 'seeds', 'peers']]
            if not values[0]:  # Verificar al menos la versión
                messagebox.showerror("Error", "Por favor ingrese al menos la versión")
                return
            versions_tree.insert('', 'end', values=values)
            for entry in entries.values():
                entry.delete(0, END)

        def update_version():
            """Actualizar versión existente"""
            nonlocal edit_mode, editing_item
            if not edit_mode or not editing_item:
                messagebox.showwarning("Advertencia", "No hay versión seleccionada para editar")
                return
                
            values = [entries[field].get().strip() for field in ['version', 'date', 'size', 'torrent', 'magnet', 'seeds', 'peers']]
            if not values[0]:
                messagebox.showerror("Error", "Por favor ingrese al menos la versión")
                return
                
            versions_tree.item(editing_item, values=values)
            cancel_edit()
            messagebox.showinfo("Éxito", "Versión actualizada correctamente")

        # Actualizar frame de botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        
        add_version_btn = ttk.Button(btn_frame, text="Agregar Versión", command=add_version)
        add_version_btn.pack(side=LEFT, padx=5)
        
        update_version_btn = ttk.Button(btn_frame, text="Actualizar Versión", 
                                      command=update_version, state=DISABLED)
        update_version_btn.pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Cancelar Edición", 
                  command=cancel_edit).pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Guardar Cambios", 
                  command=save_versions).pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Cerrar", 
                  command=edit_window.destroy).pack(side=LEFT, padx=5)

        # Cargar versiones existentes
        program_name = self.program_list.get().replace('-details.html', '')
        html_path = os.path.join(os.path.dirname(self.programs_dir), 'subpages', 
                                program_name, f"{program_name}-{year}.html")
        
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as file:
                content = file.read()
                script_pattern = r'const data = ({.*?});'
                script_match = re.search(script_pattern, content, re.DOTALL)
                if script_match:
                    try:
                        data = json.loads(script_match.group(1))
                        for version in data.get('versions', []):
                            versions_tree.insert('', 'end', values=(
                                version.get('version', ''),
                                version.get('date', ''),
                                version.get('size', ''),
                                version.get('torrentLink', ''),
                                version.get('magnetLink', ''),
                                version.get('seeds', ''),
                                version.get('peers', '')
                            ))
                    except json.JSONDecodeError:
                        pass

    def save_year_versions(self, year, versions):
        selected_file = self.program_list.get()
        if not selected_file:
            return
        
        program_name = selected_file.replace('-details.html', '')
        subpages_dir = os.path.join(os.path.dirname(self.programs_dir), 'subpages')
        program_dir = os.path.join(subpages_dir, program_name)
        
        if not os.path.exists(program_dir):
            os.makedirs(program_dir)
        
        # Crear archivo HTML para el año
        year_file = f"{program_name}-{year}.html"
        year_path = os.path.join(program_dir, year_file)
        
        # Crear JSON de versiones
        versions_json = json.dumps({"versions": versions}, indent=4)
        
        # Generar el HTML con las versiones
        year_template = f"""<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{program_name} {year} - Versiones</title>
            <link rel="stylesheet" href="../../csscomun.css">  <!-- Ruta relativa corregida -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            <script src="../../js/torrentTrackerversiones.js"></script>  <!-- Ruta relativa corregida -->
        </head>
        <body>
            <header>
                <div class="container header-content">
                    <a href="../../index.html" class="logo">  <!-- Ruta relativa corregida -->
                        <span>⬇️</span>
                        <span>PremiumDownloads</span>
                    </a>
                    <nav>
                        <ul>
                            <li><a href="../../index.html">Inicio</a></li>  <!-- Ruta relativa corregida -->
                        </ul>
                    </nav>
                </div>
            </header>

            <div class="container">
                <a href="../../programs/{selected_file}" class="back-link">  <!-- Ruta relativa corregida -->
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

            <script>
            document.addEventListener('DOMContentLoaded', () => {{
                const data = {versions_json};
                const versionList = document.querySelector('.version-list');
                versionList.innerHTML = data.versions.map(version => `
                    <!-- ... rest of template ... -->
                `).join('');
            }});
            </script>
        </body>
        </html>"""

        with open(year_path, 'w', encoding='utf-8') as year_file:
            year_file.write(year_template)

    def search_versions(self, event):
        """Buscar versiones en el TreeView"""
        search_term = self.search_entry.get().lower()
        
        # Resetear todos los tags primero
        for item in self.versions_tree.get_children():
            self.versions_tree.item(item, tags=())
        
        # Mostrar todos los items si el término de búsqueda está vacío
        if not search_term:
            return
        
        # Buscar en todas las columnas
        for item in self.versions_tree.get_children():
            values = self.versions_tree.item(item)['values']
            found = False
            
            # Convertir todos los valores a string y buscar
            for value in values:
                if str(value).lower().find(search_term) != -1:
                    found = True
                    break
            
            if found:
                self.versions_tree.item(item, tags=('match',))
            else:
                self.versions_tree.item(item, tags=('hidden',))
        
        # Configurar colores para los resultados
        self.versions_tree.tag_configure('match', background='#ff3333', foreground='white')  # Rojo brillante
        self.versions_tree.tag_configure('hidden', background='#2b2b2b', foreground='gray')  # Oscurecer los no encontrados

    def show_message(self, title, message, level="info"):
        """Mostrar mensajes estilizados"""
        if level == "error":
            messagebox.showerror(
                title,
                message,
                icon="error"
            )
        elif level == "warning":
            messagebox.showwarning(
                title,
                message,
                icon="warning"
            )
        else:
            messagebox.showinfo(
                title,
                message,
                icon="info"
            )

def main():
    root = Tk()
    app = VersionManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()