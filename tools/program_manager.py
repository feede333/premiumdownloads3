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
        chat_frame = ttk.Frame(self.chat_tab, style='Modern.TFrame')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Título del chat con fondo y bordes redondeados
        title_frame = tk.Frame(chat_frame, bg='#2196F3', height=50)
        title_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🤖 Asistente PremiumDownloads",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg='#2196F3'
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Status indicator con animación
        self.status_label = tk.Label(
            title_frame,
            text="🟢 En línea",
            font=('Segoe UI', 10),
            fg='#E8F5E9',
            bg='#2196F3'
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Área de mensajes con estilo mejorado
        chat_container = tk.Frame(chat_frame, bg='#F5F5F5')
        chat_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.chat_area = tk.Text(
            chat_container, 
            wrap=tk.WORD, 
            height=20, 
            state='disabled',
            font=('Segoe UI', 11),
            bg='#FFFFFF',
            fg='#212121',
            padx=15,
            pady=15,
            spacing2=10,  # Espacio entre párrafos
            relief=tk.FLAT,
            borderwidth=0
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=(0, 10))

        # Scrollbar personalizado
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=self.chat_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_area.configure(yscrollcommand=scrollbar.set)

        # Frame para entrada con fondo
        input_container = tk.Frame(chat_frame, bg='#F5F5F5', height=100)
        input_container.pack(fill=tk.X, pady=10)

        input_frame = tk.Frame(input_container, bg='#F5F5F5')
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Campo de entrada mejorado
        self.chat_input = tk.Entry(
            input_frame,
            font=('Segoe UI', 11),
            bg='#FFFFFF',
            fg='#757575',
            relief=tk.FLAT,
            bd=10
        )
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10), ipady=8)
        self.chat_input.insert(0, "Escribe tu mensaje aquí...")

        # Frame para botones
        buttons_frame = tk.Frame(input_frame, bg='#F5F5F5')
        buttons_frame.pack(side=tk.RIGHT, padx=5)

        # Botones con estilo moderno
        button_style = {
            'font': ('Segoe UI', 10),
            'bd': 0,
            'relief': tk.FLAT,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }

        emoji_button = tk.Button(
            buttons_frame,
            text="😊",
            command=self.show_emoji_picker,
            bg='#E3F2FD',
            fg='#212121',
            **button_style
        )
        emoji_button.pack(side=tk.LEFT, padx=2)

        send_button = tk.Button(
            buttons_frame,
            text="📤 Enviar",
            command=self.send_message,
            bg='#2196F3',
            fg='white',
            **button_style
        )
        send_button.pack(side=tk.LEFT, padx=2)

        clear_button = tk.Button(
            buttons_frame,
            text="🗑️ Limpiar",
            command=self.clear_chat,
            bg='#FF5252',
            fg='white',
            **button_style
        )
        clear_button.pack(side=tk.LEFT, padx=2)

        # Efectos hover para botones
        for button in (emoji_button, send_button, clear_button):
            button.bind('<Enter>', lambda e, b=button: b.configure(bg='#1976D2' if b == send_button else '#D32F2F' if b == clear_button else '#BBDEFB'))
            button.bind('<Leave>', lambda e, b=button: b.configure(bg='#2196F3' if b == send_button else '#FF5252' if b == clear_button else '#E3F2FD'))

        # Bindings
        self.chat_input.bind('<FocusIn>', self.on_entry_click)
        self.chat_input.bind('<FocusOut>', self.on_focus_out)
        self.chat_input.bind('<Return>', lambda e: self.send_message())

        # Mensajes con estilos mejorados
        def configure_tags(self):
            self.chat_area.tag_configure(
                'bot',
                background='#E3F2FD',
                lmargin1=20,
                lmargin2=20,
                rmargin=20,
                spacing1=10,
                spacing3=10
            )
            self.chat_area.tag_configure(
                'user',
                background='#F5F5F5',
                lmargin1=20,
                lmargin2=20,
                rmargin=20,
                spacing1=10,
                spacing3=10
            )

        configure_tags(self)

        # Mensaje inicial con estilo mejorado
        self.add_bot_message(
            "👋 ¡Hola! Soy el asistente de PremiumDownloads.\n\n" +
            "💡 Puedo ayudarte con:\n" +
            "• ℹ️ Información sobre programas\n" +
            "• 📥 Descargas y actualizaciones\n" +
            "• 🛠️ Soporte técnico\n\n" +
            "¿En qué puedo ayudarte hoy?"
        )

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
                pass  # evita error de bloque vacío
            except Exception as e:
                print(f'Error: {e}')
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

            # Validar campos requeridos
            if not all([data["id"], data["title"], data["category"]]):
                messagebox.showerror("Error", "Los campos ID, Título y Categoría son obligatorios.")
                return

            # Configurar rutas base
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            programs_dir = os.path.join(base_dir, 'programs')
            os.makedirs(programs_dir, exist_ok=True)

            # Preparar ID y nombre del programa
            program_id = data["id"].lower().replace(' ', '-')
            program_name = data["title"]

            # Manejar la imagen con rutas diferentes para index y detail
            if hasattr(self, 'image_path') and self.image_path:
                try:
                    images_dir = os.path.join(base_dir, 'images')
                    os.makedirs(images_dir, exist_ok=True)
                    
                    _, extension = os.path.splitext(self.image_path)
                    image_filename = f"{program_id}{extension}"
                    image_dest = os.path.join(images_dir, image_filename)
                    shutil.copy2(self.image_path, image_dest)
                    
                    # Rutas diferentes para index y detail
                    image_path_index = f"./images/{image_filename}"
                    image_path_detail = f"../images/{image_filename}"
                    
                    print(f"✅ Imagen copiada: {image_dest}")
                except Exception as e:
                    print(f"⚠️ Error al procesar imagen: {str(e)}")
                    image_path_index = "./images/default.png"
                    image_path_detail = "../images/default.png"
            else:
                image_path_index = "./images/default.png"
                image_path_detail = "../images/default.png"

            # Crear una versión corta de la descripción para el index
            description_full = data.get("description", "Sin descripción disponible.")
            description_short = description_full[:150] + "..." if len(description_full) > 150 else description_full

            # Actualizar el JSON con ambas descripciones
            program_data = {
                "id": program_id,
                "title": program_name,
                "category": data["category"],
                "date": datetime.now().strftime("%d.%m.%Y"),
                "image": image_path_index,
                "image_detail": image_path_detail,
                "description_short": description_short,
                "description_full": description_full,
                "description": data.get("description", ""),
            }

            # Actualizar lista de programas
            json_path = self.get_json_path()
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    programs_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                programs_data = {"programs": []}

            programs = programs_data.get("programs", [])
            program_index = next((i for i, p in enumerate(programs) 
                                if p["id"] == program_id), None)
            
            if program_index is not None:
                programs[program_index] = program_data
            else:
                programs.append(program_data)

            programs_data["programs"] = programs

            # Guardar JSON actualizado
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(programs_data, f, indent=2, ensure_ascii=False)

            # Actualizar el template HTML con todos los detalles
            html_template = f"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{program_name} - Descarga | PremiumDownloads</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="../css/detail.css">
    <link rel="stylesheet" href="../css/commentcss.css">
    <link rel="stylesheet" href="../css/chat.css">
    <script src="../js/detailuniversal.js" defer></script>
    <script src="../js/main.js" defer></script>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="../index.html" class="logo">
                    <span>⬇️</span>
                    <span>PremiumDownloads</span>
                </a>
                <nav>
                    <ul>
                        <li><a href="../index.html">Inicio</a></li>
                        <li><a href="../populares.html">Populares</a></li>
                    </ul>
                </nav>
                <div class="theme-language-controls">
                    <button class="theme-toggle">
                        <i class="fas fa-moon"></i>
                    </button>
                    <button class="language-toggle">
                        <span class="lang-text">ES</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <a href="../index.html" class="back-link">
            <i class="fa fa-arrow-left"></i> Volver a todos los programas
        </a>

        <div class="download-detail">
            <div class="download-header">
                <div class="download-image">
                    <img src="{image_path_detail}" alt="{program_name}">
                </div>
                <div class="download-info">
                    <h1 class="download-title">{program_name}</h1>
                    <span class="download-category">{data['category']}</span>
                    
                    <div class="download-meta">
                        <div class="meta-item meta-size">
                            <i class="fas fa-download"></i>
                            <span>{data.get('fileSize', 'N/A')}</span>
                        </div>
                        <div class="meta-item meta-date">
                            <i class="fas fa-calendar-alt"></i>
                            <span>{datetime.now().strftime('%d.%m.%Y')}</span>
                        </div>
                    </div>
                    
                    <div class="download-description">
                        <p>{data.get('description', 'Sin descripción disponible.')}</p>
                    </div>
                </div>
            </div>

            <div class="download-versions">
                <h3 class="versions-title">Versiones por año</h3>
                <ul class="version-years">
                    <!-- AÑOS-START -->
                    <!-- Se actualizará dinámicamente -->
                    <!-- AÑOS-END -->
                </ul>
            </div>

            <div class="requirements">
                <h3>Requisitos del sistema</h3>
                <ul>
                    <li>Sistema operativo: {data.get('os', 'N/A')}</li>
                    <li>Procesador: {data.get('processor', 'N/A')}</li>
                    <li>Memoria RAM: {data.get('ram', 'N/A')}</li>
                    <li>Espacio en disco: {data.get('disk', 'N/A')}</li>
                    <li>Resolución de pantalla: {data.get('display', 'N/A')}</li>
                </ul>
            </div>

            <section class="comments-section">
                <h3>Comentarios</h3>
                
                <form id="comment-form" class="comment-form" aria-label="Formulario de comentarios">
                    <div class="form-row">
                        <input type="text" id="comment-name" placeholder="Tu nombre" required
                            class="comment-input" aria-label="Nombre">
                        <input type="email" id="user-email" placeholder="Correo electrónico (opcional)" 
                            class="comment-input email-input" aria-label="Correo electrónico">
                    </div>
                
                    <div class="image-upload-container">
                        <input type="file" id="comment-image" accept="image/*" hidden>
                        <label for="comment-image" class="photo-icon">
                            <i class="fas fa-camera"></i> Agregar foto
                        </label>
                        <div class="image-preview"></div>
                    </div>
                
                    <textarea id="comment-text" placeholder="Escribe tu comentario..." required
                        class="comment-textarea" aria-label="Comentario"></textarea>
                    
                    <div class="captcha-container">
                        <div class="captcha-box">
                            <span id="captcha-text"></span>
                            <button type="button" id="refresh-captcha" class="refresh-captcha">
                                <i class="fas fa-sync-alt"></i>
                            </button>
                        </div>
                        <input type="text" id="captcha-input" placeholder="Ingresa el código" required
                            class="captcha-input" aria-label="Verificación CAPTCHA">
                        <span id="captcha-error" class="captcha-error"></span>
                    </div>

                    <button type="submit" class="comment-submit">Publicar</button>
                </form>
                
                <div id="comments-list" class="comments-list">
                    <!-- Los comentarios aparecerán aquí -->
                </div>
            </section>
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

    <div class="ai-chat-widget">
        <button class="chat-toggle">
            <i class="fas fa-robot"></i>
        </button>
        <div class="chat-container">
            <div class="chat-header">
                <h3>Asistente IA</h3>
                <button class="close-chat">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="chat-messages">
                <div class="message bot">
                    ¡Hola! Soy el asistente virtual. ¿En qué puedo ayudarte?
                </div>
            </div>
            <div class="chat-input-container">
                <input type="text" class="chat-input" placeholder="Escribe tu mensaje...">
                <button class="send-message">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>
</body>
</html>"""

            # Guardar el archivo HTML
            details_path = os.path.join(programs_dir, f"{program_id}-details.html")
            with open(details_path, "w", encoding="utf-8") as f:
                f.write(html_template)
            print(f"✅ Archivo HTML creado: {details_path}")

            # Actualizar la lista de programas en la interfaz
            self.load_existing_programs()
            
            # Agregar sincronización con GitHub
            try:
                commit_message = f"Add: Nuevo programa {program_name}"
                self.sync_with_github(commit_message)
                print("✅ Cambios sincronizados con GitHub")
            except Exception as git_error:
                print(f"⚠️ Error en la sincronización con GitHub: {str(git_error)}")
                # No interrumpimos el flujo si falla la sincronización
            
            messagebox.showinfo("Éxito", "Programa guardado correctamente y sincronizado con GitHub")

        except Exception as e:
            error_msg = f"Error al guardar el programa: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)

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
            Genera un JSON con la siguiente estructura para el programa de software:
            {{"id": "{program_id}",
             "title": "{program_title}",
             "category": "Diseño",
             "version": "string",
             "fileSize": "string",
             "description": "string",
             "requirements": {{
                "os": "string",
                "processor": "string",
                "ram": "string",
                "disk": "string",
                "display": "string"
             }},
             "instructions": "string"
            }}

            Proporciona información detallada y técnica, incluyendo:
            - Descripción técnica completa con características y beneficios
            - Versión más reciente
            - Tamaño aproximado del instalador
            - Requisitos mínimos y recomendados
            - Instrucciones paso a paso para instalación y activación
            """

            # Llamar a la API de DeepSeek con el formato correcto
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un experto en software que genera información técnica precisa en formato JSON. Mantén la estructura exacta del JSON solicitado."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.5,  # Menos aleatorio
                "max_tokens": 2000,  # Más tokens para respuestas completas
                "top_p": 0.9,
                "stream": False
            }

            print("Enviando solicitud con datos:", data)  # Debug
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            print(f"Código de respuesta: {response.status_code}")  # Debug
            response.raise_for_status()
            
            result = response.json()
            print("Respuesta recibida:", result)  # Debug
            
            # Procesar la respuesta
            try:
                generated_data = json.loads(result['choices'][0]['message']['content'])
                print("Datos generados:", generated_data)  # Debug
                
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

            except json.JSONDecodeError as e:
                print("Error decodificando JSON:", str(e))
                print("Contenido recibido:", result['choices'][0]['message']['content'])
                messagebox.showerror("Error", "La IA no generó un JSON válido")

        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = f"Error al autocompletar: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)

    def get_json_path(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'data', 'programs.json')  # Directamente en la raíz

    def add_version(self, program_id, year):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            subpages_dir = os.path.join(base_dir, 'subpages', program_id)
            os.makedirs(subpages_dir, exist_ok=True)

            file_name = f"{year}.html"
            file_path = os.path.join(subpages_dir, file_name)

            # Crear archivo HTML con referencia al csscomun.css
            css_path = os.path.join(base_dir, 'subpages', 'csscomun.css')
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{program_id} {year} - Versiones</title>
    <link rel="stylesheet" href="../csscomun.css">
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
        <h2>Versiones de {year}</h2>
        <div class="version-list">
            <!-- Las versiones se cargarán dinámicamente -->
        </div>
    </div>

    <footer>
        <div class="container">
            <p>© {datetime.now().year} PremiumDownloads. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>""")
            print(f"✅ Archivo de versión creado: {file_path}")

            messagebox.showinfo("Éxito", f"Versión {year} creada correctamente para {program_id}.")

        except Exception as e:
            error_msg = f"Error al crear la versión: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)

    def create_program_structure(self, program_name):
        try:
            # Validar nombre del programa
            if not self.validate_program_name(program_name):
                return False

            # Normalizar el nombre del programa para usarlo en rutas
            program_id = program_name.lower().replace(' ', '-')
            
            # Crear carpeta específica del programa en subpages
            program_subpages = os.path.join(self.subpages_path, program_id)
            os.makedirs(program_subpages, exist_ok=True)

            # Crear archivo details.html
            self.create_details_file(program_name, program_id)

            print(f"✅ Estructura creada para {program_name}:")
            print(f"  📁 Carpeta: {program_subpages}")
            print(f"  📄 Details: {os.path.join(self.programs_path, f'{program_id}-details.html')}")

            # Actualizar index.html
            self.update_index_page()

            # Sincronizar con GitHub
            self.sync_with_github(f"Add: Nuevo programa {program_name}")

            return program_id

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la estructura: {str(e)}")
            return False

    def update_index_page(self):
        try:
            index_path = os.path.join(self.base_path, "index.html")
            
            # Obtener lista de programas
            programs = []
            for file in os.listdir(self.programs_path):
                if file.endswith("-details.html"):
                    program_id = file.replace("-details.html", "")
                    program_name = program_id.replace("-", " ").title()
                    
                    # Obtener años disponibles
                    years = self.list_html_files(program_id)
                    version_count = len(years)
                    
                    programs.append({
                        "id": program_id,
                        "name": program_name,
                        "details_url": f"programs/{file}",  # Enlace al details.html específico
                        "version_count": version_count,
                        "latest_year": max(years).replace(".html", "") if years else "N/A",
                        "image": f"./images/{program_id}.png" if os.path.exists(f"./images/{program_id}.png") else "./images/default.png",
                        "description_short": "Descripción breve del programa"  # Ejemplo de descripción corta
                    })

            # Leer plantilla del index
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Encontrar la sección donde se insertan los programas
            start_marker = '<!-- PROGRAMS-START -->'
            end_marker = '<!-- PROGRAMS-END -->'
            start = content.find(start_marker)
            end = content.find(end_marker)

            if (start == -1) or (end == -1):
                raise ValueError("No se encontraron los marcadores en index.html")

            # Generar HTML para cada programa
            programs_html = []
            for program in sorted(programs, key=lambda x: x["name"]):
                programs_html.append(f'''
                    <div class="program-card">
                        <div class="program-image">
                            <img src="{program.get('image', './images/default.png')}" alt="{program['name']}">
                        </div>
                        <div class="program-content">
                            <h3>{program["name"]}</h3>
                            <p class="program-description">{program.get('description_short', '')}</p>
                            <div class="program-meta">
                                <span>Versiones: {program["version_count"]}</span>
                                <span>Última: {program["latest_year"]}</span>
                            </div>
                            <a href="{program["details_url"]}" class="program-link">
                                Ver detalles <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                ''')

            # Insertar el nuevo contenido
            new_content = (
                content[:start + len(start_marker)] +
                '\n' +
                ''.join(programs_html) +
                '\n' +
                content[end:]
            )

            # Guardar cambios
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print("✅ Index.html actualizado correctamente")
            return True

        except Exception as e:
            print(f"❌ Error actualizando index.html: {str(e)}")
            messagebox.showerror("Error", f"Error actualizando index.html: {str(e)}")
            return False

if __name__ == "__main__":
    verify_setup()
    root = tk.Tk()
    app = ProgramManagerApp(root)
    root.mainloop()