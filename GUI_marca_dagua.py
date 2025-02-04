import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de Marca d'Água")
        self.root.geometry("800x600")

        self.image_path = None
        self.image = None
        self.logo_path = None
        self.logo = None
        self.watermarked_image = None
        self.watermark_type = tk.StringVar(value="logo")  # Opções: 'logo' ou 'text'

        self.text_watermark = "Texto Padrão"
        self.text_position = (50, 50)
        self.text_color = "white"
        self.font_size = 30

        self.logo_position = (50, 50)
        self.dragging = False

        # Botões
        tk.Button(root, text="Carregar Imagem", command=self.load_image).pack(pady=5)
        tk.Button(root, text="Carregar Logotipo", command=self.load_logo).pack(pady=5)
        tk.Button(root, text="Escolher Cor do Texto", command=self.choose_text_color).pack(pady=5)

        # Alternância entre logotipo e texto
        tk.Label(root, text="Escolha a marca d'água:").pack()
        tk.Radiobutton(root, text="Logotipo", variable=self.watermark_type, value="logo").pack()
        tk.Radiobutton(root, text="Texto", variable=self.watermark_type, value="text").pack()

        # Entrada para o texto
        tk.Label(root, text="Texto da marca d'água:").pack()
        self.text_entry = tk.Entry(root)
        self.text_entry.pack()
        self.text_entry.insert(0, self.text_watermark)

        # Transparência
        self.alpha_var = tk.DoubleVar(value=0.5)
        tk.Label(root, text="Transparência:").pack()
        tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, orient="horizontal", variable=self.alpha_var).pack()

        # Aplicar marca d'água e salvar
        tk.Button(root, text="Aplicar Marca d'Água", command=self.apply_watermark).pack(pady=5)
        tk.Button(root, text="Salvar Imagem", command=self.save_image).pack(pady=5)

        # Área de exibição
        self.canvas = tk.Canvas(root, width=600, height=400, bg="gray")
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.image = Image.open(self.image_path).convert("RGBA")
            self.display_image(self.image)

    def load_logo(self):
        self.logo_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if self.logo_path:
            self.logo = Image.open(self.logo_path).convert("RGBA")
            self.display_image(self.logo, is_logo=True)

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Escolha a cor do texto")
        if color[1]:
            self.text_color = color[1]

    def apply_watermark(self):
        if self.image is None:
            messagebox.showerror("Erro", "Carregue uma imagem primeiro.")
            return

        self.watermarked_image = self.image.copy()
        draw = ImageDraw.Draw(self.watermarked_image)

        if self.watermark_type.get() == "logo":
            if self.logo is None:
                messagebox.showerror("Erro", "Carregue um logotipo primeiro.")
                return

            img_w, img_h = self.image.size
            scale_factor = img_w // 5
            self.logo = self.logo.resize((scale_factor, int((scale_factor / self.logo.width) * self.logo.height)),
                                         Image.LANCZOS)

            alpha = self.alpha_var.get()
            logo_transparent = self.logo.copy()
            logo_transparent.putalpha(int(255 * alpha))
            self.watermarked_image.paste(logo_transparent, self.logo_position, logo_transparent)

        elif self.watermark_type.get() == "text":
            font = ImageFont.truetype("arial.ttf", self.font_size)
            alpha = int(255 * self.alpha_var.get())
            draw.text(self.text_position, self.text_entry.get(), fill=self.text_color + hex(alpha)[2:], font=font)

        self.display_image(self.watermarked_image)

    def display_image(self, img, is_logo=False):
        img.thumbnail((300, 200)) if is_logo else img.thumbnail((600, 400))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(300, 200, image=self.tk_image, anchor="center")

    def start_drag(self, event):
        self.dragging = True
        if self.watermark_type.get() == "logo":
            self.logo_position = (event.x, event.y)
        elif self.watermark_type.get() == "text":
            self.text_position = (event.x, event.y)
        self.apply_watermark()

    def drag(self, event):
        if self.dragging:
            if self.watermark_type.get() == "logo":
                self.logo_position = (event.x, event.y)
            elif self.watermark_type.get() == "text":
                self.text_position = (event.x, event.y)
            self.apply_watermark()

    def save_image(self):
        if self.watermarked_image is None:
            messagebox.showerror("Erro", "Nenhuma imagem processada para salvar.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"),
                                                            ("Todos os Arquivos", "*.*")])
        if save_path:
            self.watermarked_image.save(save_path)
            messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")


# Executa o aplicativo
root = tk.Tk()
app = WatermarkApp(root)
root.mainloop()
