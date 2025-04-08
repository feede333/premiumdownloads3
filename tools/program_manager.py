import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
from datetime import datetime

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise EnvironmentError("GITHUB_TOKEN environment variable not found. Please set it in your system environment variables.")

class ProgramManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Programas - PremiumDownloads")
        self.root.geometry("600x800")

        # Crear el formulario
        self.create_form()

    def create_form(self):
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root)
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

        # Botón para guardar
        ttk.Button(self.scrollable_frame, text="Guardar programa", 
                  command=self.save_program).pack(pady=20)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

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


            # Actualizar rutas para usar frontend/public
            base_dir = os.path.dirname(os.path.abspath(__file__))
            repo_dir = os.path.dirname(base_dir)
            frontend_dir = os.path.join(repo_dir, 'frontend', 'public')
            data_dir = os.path.join(frontend_dir, 'data')
            images_dir = os.path.join(frontend_dir, 'images')
            
            print(f"\nDirectorios:")
            print(f"Base: {base_dir}")
            print(f"Repo: {repo_dir}")
            print(f"Frontend: {frontend_dir}")
            print(f"Data: {data_dir}")
            print(f"Images: {images_dir}")

            # Crear directorios
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

            # Manejar imagen si se proporcionó
            if hasattr(self, 'image_path') and self.image_path:
                image_filename = f"{data['id']}{os.path.splitext(self.image_path)[1]}"
                image_dest = os.path.join(images_dir, image_filename)
                shutil.copy2(self.image_path, image_dest)
                program_data["image"] = f"/premiumdownloads3/images/{image_filename}"
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramManagerApp(root)
    root.mainloop()