import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
from datetime import datetime
import requests

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise EnvironmentError("GITHUB_TOKEN environment variable not found. Please set it in your system environment variables.")

def verify_setup():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar estructura de directorios en la raíz
    paths_to_check = [
        'data',
        'images',
        'js',
        'css'
    ]
    
    for path in paths_to_check:
        full_path = os.path.join(base_dir, path)
        if not os.path.exists(full_path):
            print(f"⚠️ Creando directorio faltante: {path}")
            os.makedirs(full_path)

class ProgramManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Programas - PremiumDownloads")
        self.root.geometry("600x800")
        
        # Configurar DeepSeek con la API key directamente
        self.deepseek_api_key = "sk-84b4c6e1bd82482cb5c131a45acb7d8b"
        print(f"API Key configurada: {'Sí' if self.deepseek_api_key else 'No'}")

        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Pestaña para agregar programas
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Agregar Programa")

        # Pestaña para gestionar programas
        self.manage_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_tab, text="Gestionar Programas")

        # Pestaña para el chatbot
        self.chat_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_tab, text="ChatBot")

        # Crear componentes
        self.create_form()
        self.create_programs_list()
        self.create_chatbot()

    def create_form(self):
        # Frame principal con scroll
        main_frame = ttk.Frame(self.add_tab)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Campos del formulario
        fields = [
            ("ID del programa:", "id"),
            ("Título:", "title"),
            ("Categoría:", "category", "combo", ["Diseño", "Seguridad", "Multimedia", "Utilidades", "Productividad"]),
            ("Versión:", "version"),
            ("Tamaño del archivo:", "fileSize"),
            ("Enlace de descarga:", "downloadLink"),
            ("Descripción:", "description", "text"),
            ("Sistema operativo:", "os"),
            ("Procesador:", "processor"),
            ("RAM:", "ram"),
            ("Espacio en disco:", "disk"),
            ("Pantalla:", "display"),
            ("Instrucciones:", "instructions", "text")
        ]

        self.entries = {}
        
        for field in fields:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            label = ttk.Label(frame, text=field[0])
            label.pack(side=tk.LEFT)
            
            if len(field) > 2:
                if field[2] == "text":
                    entry = tk.Text(frame, height=4, width=40)
                elif field[2] == "combo":
                    entry = ttk.Combobox(frame, values=field[3], width=37)
                    entry.set(field[3][0])
            else:
                entry = ttk.Entry(frame, width=40)
            entry.pack(side=tk.LEFT, padx=5)
            
            self.entries[field[1]] = entry

        # Botón para seleccionar imagen
        ttk.Button(self.scrollable_frame, text="Seleccionar imagen", 
                  command=self.select_image).pack(pady=5)

        # Agregar botón de autocompletar antes del botón guardar
        if self.deepseek_api_key:
            autocomplete_button = ttk.Button(
                self.scrollable_frame, 
                text="🤖 Autocompletar con IA", 
                command=self.autocomplete_with_ai
            )
            autocomplete_button.pack(pady=5)

        # Botón para guardar
        ttk.Button(self.scrollable_frame, text="Guardar programa", 
                  command=self.save_program).pack(pady=20)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def create_programs_list(self):
        # Frame con scroll para la lista
        list_frame = ttk.Frame(self.manage_tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear Treeview
        columns = ('ID', 'Título', 'Categoría', 'Fecha')
        self.programs_tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='extended')
        
        # Configurar columnas
        for col in columns:
            self.programs_tree.heading(col, text=col)
            self.programs_tree.column(col, width=100)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.programs_tree.yview)
        self.programs_tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar elementos
        self.programs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones para eliminar
        buttons_frame = ttk.Frame(self.manage_tab)
        buttons_frame.pack(pady=5)
        
        delete_button = ttk.Button(buttons_frame, text="Eliminar Seleccionados", command=self.delete_program)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        delete_all_button = ttk.Button(buttons_frame, text="Eliminar Todo", command=self.delete_all_programs)
        delete_all_button.pack(side=tk.LEFT, padx=5)

        # Cargar programas existentes
        self.load_existing_programs()

    def create_chatbot(self):
        # Frame principal del chat con estilo moderno
        chat_frame = ttk.Frame(self.chat_tab)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Título del chat
        title_frame = ttk.Frame(chat_frame)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        
        title_label = ttk.Label(title_frame, text="🤖 Asistente PremiumDownloads", font=('Helvetica', 12, 'bold'))
        title_label.pack(side=tk.LEFT)

        # Status indicator
        self.status_label = ttk.Label(title_frame, text="🟢 En línea", foreground='green')
        self.status_label.pack(side=tk.RIGHT)

        # Área de mensajes con estilo
        self.chat_area = tk.Text(
            chat_frame, 
            wrap=tk.WORD, 
            height=20, 
            state='disabled',
            font=('Helvetica', 10),
            bg='#f5f5f5',
            padx=10,
            pady=10
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para entrada y botones
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Campo de entrada con placeholder
        self.chat_input = ttk.Entry(input_frame, width=50)
        self.chat_input.insert(0, "Escribe tu mensaje aquí...")
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Efecto placeholder
        self.chat_input.bind('<FocusIn>', self.on_entry_click)
        self.chat_input.bind('<FocusOut>', self.on_focus_out)

        # Botones con emojis
        emoji_button = ttk.Button(input_frame, text="😊", width=3, command=self.show_emoji_picker)
        emoji_button.pack(side=tk.LEFT, padx=2)

        send_button = ttk.Button(input_frame, text="📤 Enviar", command=self.send_message)
        send_button.pack(side=tk.LEFT, padx=2)

        clear_button = ttk.Button(input_frame, text="🗑️ Limpiar", command=self.clear_chat)
        clear_button.pack(side=tk.LEFT, padx=2)

        # Bind Enter key
        self.chat_input.bind('<Return>', lambda e: self.send_message())

        # Mensaje inicial con emojis
        self.add_bot_message("👋 ¡Hola! Soy el asistente de PremiumDownloads. \n\n💡 Puedo ayudarte con:\n• ℹ️ Información sobre programas\n• 📥 Descargas\n• 🛠️ Soporte técnico\n\n¿En qué puedo ayudarte hoy?")

    def on_entry_click(self, event):
        """Función para manejar el placeholder del input"""
        if self.chat_input.get() == 'Escribe tu mensaje aquí...':
            self.chat_input.delete(0, tk.END)
            self.chat_input.config(foreground='black')

    def on_focus_out(self, event):
        """Función para restaurar el placeholder"""
        if self.chat_input.get() == '':
            self.chat_input.insert(0, 'Escribe tu mensaje aquí...')
            self.chat_input.config(foreground='gray')

    def clear_chat(self):
        """Función para limpiar el chat"""
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar todo el historial del chat?"):
            self.chat_area.config(state='normal')
            self.chat_area.delete(1.0, tk.END)
            self.chat_area.config(state='disabled')
            self.add_bot_message("💬 Chat limpiado. ¿En qué puedo ayudarte?")

    def show_emoji_picker(self):
        """Muestra un selector de emojis común"""
        emojis = ["😊", "👍", "❤️", "🎮", "💻", "🔥", "👀", "💡", "⭐", "✅"]
        
        # Crear ventana emergente
        popup = tk.Toplevel(self.root)
        popup.title("Emojis")
        popup.geometry("200x150")
        
        def insert_emoji(emoji):
            current = self.chat_input.get()
            if current == "Escribe tu mensaje aquí...":
                current = ""
            self.chat_input.delete(0, tk.END)
            self.chat_input.insert(0, current + emoji)
            popup.destroy()

        # Crear grid de emojis
        for i, emoji in enumerate(emojis):
            btn = ttk.Button(popup, text=emoji, command=lambda e=emoji: insert_emoji(e))
            btn.grid(row=i//5, column=i%5, padx=2, pady=2)

    def add_bot_message(self, message):
        """Función mejorada para mensajes del bot"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "\n🤖 Bot: " + message + "\n", 'bot')
        self.chat_area.tag_configure('bot', background='#e3f2fd', lmargin1=20, lmargin2=20, rmargin=20)
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def add_user_message(self, message):
        """Función mejorada para mensajes del usuario"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "\n👤 Tú: " + message + "\n", 'user')
        self.chat_area.tag_configure('user', background='#f5f5f5', lmargin1=20, lmargin2=20, rmargin=20)
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self):
        message = self.chat_input.get().strip()
        if not message or message == "Escribe tu mensaje aquí...":
            return

        self.add_user_message(message)
        self.chat_input.delete(0, tk.END)
        self.chat_input.insert(0, "Escribe tu mensaje aquí...")
        self.chat_input.config(foreground='gray')

        try:
            # Llamar a la API de DeepSeek con el formato correcto
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",  # Especificar el modelo
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en software y tecnología que ayuda a los usuarios con información sobre programas, descargas y soporte técnico."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 1,
                "stream": False
            }

            print("Enviando solicitud a DeepSeek...")
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30  # Agregar timeout
            )

            print(f"Código de respuesta: {response.status_code}")
            response.raise_for_status()
            
            result = response.json()
            print("Respuesta recibida:", result)
            
            bot_response = result['choices'][0]['message']['content']
            self.add_bot_message(bot_response)

        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(f"❌ {error_msg}")
            self.add_bot_message(f"Lo siento, hubo un problema de conexión. Por favor, intenta de nuevo.")
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ {error_msg}")
            self.add_bot_message(f"Lo siento, ocurrió un error. Por favor, intenta de nuevo más tarde.")

    def load_existing_programs(self):
        try:
            # Limpiar árbol
            for item in self.programs_tree.get_children():
                self.programs_tree.delete(item)

            json_path = self.get_json_path()
            print(f"Cargando programas desde: {json_path}")

            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    programs = data.get('programs', [])
                    print(f"Programas encontrados: {len(programs)}")
                    
                    for program in programs:
                        self.programs_tree.insert('', tk.END, values=(
                            program['id'],
                            program['title'],
                            program['category'],
                            program.get('date', 'N/A')
                        ))
                        print(f"Programa cargado: {program['title']}")
        except Exception as e:
            print(f"Error cargando programas: {str(e)}")
            messagebox.showerror("Error", f"Error cargando programas: {str(e)}")

    def delete_program(self):
        selected_items = self.programs_tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Seleccione al menos un programa para eliminar")
            return

        programs_to_delete = len(selected_items)
        if programs_to_delete == 1:
            message = "¿Está seguro de eliminar este programa?"
        else:
            message = f"¿Está seguro de eliminar estos {programs_to_delete} programas?"

        if messagebox.askyesno("Confirmar", message):
            try:
                # Obtener ruta del JSON desde la raíz
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                json_path = os.path.join(base_dir, 'data', 'programs.json')
                
                # Leer JSON actual
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    programs = data.get('programs', [])
                    
                # Obtener IDs de programas seleccionados
                program_ids = [self.programs_tree.item(item)['values'][0] for item in selected_items]
                print(f"Intentando eliminar programas con IDs: {program_ids}")
                
                # Guardar cantidad anterior
                prev_count = len(programs)
                
                # Filtrar programas
                data['programs'] = [p for p in programs if str(p.get('id', '')).strip() not in 
                                  [str(pid).strip() for pid in program_ids]]
                
                # Verificar eliminación
                new_count = len(data['programs'])
                deleted_count = prev_count - new_count
                print(f"Programas antes: {prev_count}, después: {new_count}")
                
                if deleted_count == 0:
                    print("⚠️ No se encontraron programas para eliminar")
                    return
                
                # Guardar JSON actualizado
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("✅ JSON actualizado")
                
                # Eliminar imágenes
                for program_id in program_ids:
                    image_path = os.path.join(base_dir, 'images', f"{program_id}.png")
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print(f"✅ Imagen eliminada: {image_path}")
                
                # Actualizar lista
                self.load_existing_programs()
                print("✅ Lista actualizada")
                
                # Sincronizar con GitHub
                commit_msg = f"Remove: {deleted_count} programa{'s' if deleted_count > 1 else ''}"
                self.sync_with_github(commit_msg)
                
                messagebox.showinfo("Éxito", 
                    f"{deleted_count} programa{'s' if deleted_count > 1 else ''} eliminado{'s' if deleted_count > 1 else ''} correctamente")
                
            except Exception as e:
                error_msg = f"Error al eliminar programas: {str(e)}"
                print(f"❌ {error_msg}")
                messagebox.showerror("Error", error_msg)

    def delete_all_programs(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar TODOS los programas?",
                              icon='warning'):
            try:
                # Seleccionar todos los items
                self.programs_tree.selection_set(self.programs_tree.get_children())
                # Usar el método existente para eliminar
                self.delete_program()
            except Exception as e:
                error_msg = f"Error al eliminar todos los programas: {str(e)}"
                print(f"❌ {error_msg}")
                messagebox.showerror("Error", error_msg)

    def sync_with_github(self, commit_message):
        try:
            import subprocess
            
            if not token:
                raise EnvironmentError("Token de GitHub no encontrado")

            # Obtener el directorio raíz del repositorio
            repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print(f"Sincronizando desde: {repo_dir}")

            repo_url = f"https://{token}@github.com/feede333/premiumdownloads3.git"
            
            # Usar repo_dir como directorio de trabajo
            subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], cwd=repo_dir, check=True)
            subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_dir, check=True)
            subprocess.run(['git', 'pull', 'origin', 'main', '--rebase'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, check=True)
            
            print("✅ Cambios sincronizados con GitHub")

        except Exception as e:
            print(f"❌ Error sincronizando con GitHub: {str(e)}")
            raise

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
        )

    def save_program(self):
        try:
            print("\n=== Inicio del proceso de guardado ===")
            
            # Recopilar datos del formulario
            data = {}
            for key, entry in self.entries.items():
                if isinstance(entry, tk.Text):
                    data[key] = entry.get("1.0", tk.END).strip()
                else:
                    data[key] = entry.get().strip()
                print(f"Campo {key}: {data[key]}")  # Debug

            # Validar campos requeridos
            if not all([data["id"], data["title"], data["category"]]):
                messagebox.showerror("Error", "Los campos ID, título y categoría son obligatorios")
                return

            # Usar las mismas rutas que update.bat
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, 'data')  # Directamente en la raíz
            images_dir = os.path.join(base_dir, 'images')  # Directamente en la raíz
            
            print(f"\nDirectorios:")
            print(f"Base: {base_dir}")
            print(f"Data: {data_dir}")
            print(f"Images: {images_dir}")

            # Crear directorios si no existen
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)

            # Preparar datos del programa
            program_data = {
                "id": data["id"],
                "title": data["title"],
                "category": data["category"],
                "version": data["version"],
                "fileSize": data["fileSize"],
                "downloadLink": data["downloadLink"],
                "date": datetime.now().strftime("%d.%m.%Y"),
                "image": "images/default.png",  # Valor por defecto
                "description": data["description"],
                "requirements": {
                    "os": data["os"],
                    "processor": data["processor"],
                    "ram": data["ram"],
                    "disk": data["disk"],
                    "display": data["display"]
                },
                "instructions": data["instructions"]
            }

            # Actualizar ruta de imagen para que coincida con index.html
            if hasattr(self, 'image_path') and self.image_path:
                image_filename = f"{data['id']}{os.path.splitext(self.image_path)[1]}"
                image_dest = os.path.join(images_dir, image_filename)
                shutil.copy2(self.image_path, image_dest)
                program_data["image"] = f"./images/{image_filename}"  # Usar ruta relativa como en index.html
                print(f"\nImagen copiada a: {image_dest}")

            # Guardar JSON
            json_path = os.path.join(data_dir, "programs.json")
            print(f"\nGuardando en JSON: {json_path}")

            # Cargar o crear JSON
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    programs_data = json.load(f)
                    print(f"JSON existente cargado con {len(programs_data.get('programs', []))} programas")
            else:
                programs_data = {"programs": []}
                print("Creando nuevo archivo JSON")

            # Añadir nuevo programa
            programs_data["programs"].append(program_data)
            
            # Guardar JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(programs_data, f, indent=2, ensure_ascii=False)
            
            print(f"\nJSON guardado. Tamaño: {os.path.getsize(json_path)} bytes")
            
            # Generar páginas HTML
            print("\n=== Generando páginas HTML ===")
            try:
                import page_generator
                generator = page_generator.PageGenerator()
                generator.update_pages()
                print("✅ Páginas HTML generadas")
            except Exception as e:
                print(f"❌ Error generando páginas HTML: {str(e)}")
                raise

            # Sincronizar con GitHub
            print("\n=== Sincronizando con GitHub ===")
            try:
                import subprocess
                
                # Verificar el token
                if not token:
                    raise EnvironmentError("Token de GitHub no encontrado")
                print("✅ Token de GitHub encontrado")
                
                # Configurar Git con el token
                repo_url = f"https://{token}@github.com/feede333/premiumdownloads3.git"
                repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], cwd=repo_dir, check=True)
                
                # Sincronizar cambios
                print("\nSubiendo cambios a GitHub...")
                subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)
                subprocess.run(['git', 'commit', '-m', f'Add: Nuevo programa {data["title"]}'], cwd=repo_dir, check=True)
                subprocess.run(['git', 'pull', 'origin', 'main', '--rebase'], cwd=repo_dir, check=True)
                subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, check=True)
                
                print("✅ Cambios sincronizados con GitHub")
                
            except Exception as e:
                print(f"❌ Error sincronizando con GitHub: {str(e)}")
                raise

            messagebox.showinfo("Éxito", "Programa guardado y sincronizado correctamente")
            self.root.quit()

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
            raise

    def autocomplete_with_ai(self):
        try:
            # Obtener el ID y título si ya están ingresados
            program_id = self.entries["id"].get().strip()
            program_title = self.entries["title"].get().strip()

            if not program_title and not program_id:
                messagebox.showerror("Error", "Ingresa al menos el ID o título del programa")
                return

            print("Consultando a DeepSeek...")
            
            # Crear el prompt
            prompt = f"""
            Genera información detallada para un programa de software:
            {"ID: " + program_id if program_id else ""}
            {"Título: " + program_title if program_title else ""}
            
            Incluye:
            - Descripción técnica y beneficios
            - Categoría (entre: Diseño, Seguridad, Multimedia, Utilidades, Productividad)
            - Versión actual
            - Tamaño aproximado
            - Requisitos del sistema (OS, CPU, RAM, Disco)
            - Instrucciones de instalación paso a paso
            
            Formato JSON.
            """

            # Llamar a la API de DeepSeek
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messages": [
                    {"role": "system", "content": "Eres un experto en software que proporciona información técnica precisa."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            response.raise_for_status()
            result = response.json()

            # Procesar la respuesta
            try:
                generated_data = json.loads(result['choices'][0]['message']['content'])
                
                # Rellenar los campos
                for key, value in generated_data.items():
                    if key in self.entries:
                        if isinstance(self.entries[key], tk.Text):
                            self.entries[key].delete("1.0", tk.END)
                            self.entries[key].insert("1.0", str(value))
                        else:
                            self.entries[key].delete(0, tk.END)
                            self.entries[key].insert(0, str(value))

                # Rellenar requisitos del sistema
                if "requirements" in generated_data:
                    for req_key, req_value in generated_data["requirements"].items():
                        if req_key in self.entries:
                            self.entries[req_key].delete(0, tk.END)
                            self.entries[req_key].insert(0, str(req_value))

                messagebox.showinfo("Éxito", "Datos generados correctamente")

            except json.JSONDecodeError:
                print("Respuesta no JSON:", result['choices'][0]['message']['content'])
                messagebox.showerror("Error", "La IA no generó un JSON válido")

        except Exception as e:
            error_msg = f"Error al autocompletar: {str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)

    def get_json_path(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'data', 'programs.json')  # Directamente en la raíz

if __name__ == "__main__":
    verify_setup()
    root = tk.Tk()
    app = ProgramManagerApp(root)
    root.mainloop()