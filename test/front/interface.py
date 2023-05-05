import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from RangeSlider import RangeSliderH, RangeSliderV

class RangeSliderWidget(Frame):
    def __init__(self, master, min_val, max_val, initial_range=None, **kwargs):
        super().__init__(master, bg='#D70755', **kwargs)

        self.min_val = min_val
        self.max_val = max_val
        if initial_range is None:
            initial_range = [min_val, max_val]
        self.range = initial_range

        # Création du RangeSlider horizontal pour la plage de valeurs
        self.hVar1 = DoubleVar(value=initial_range[0])
        self.hVar2 = DoubleVar(value=initial_range[1])
                # Création des entrées min et max reliées au RangeSlider
        self.min_entry = Entry(self, textvariable=self.hVar1, width=5)
        self.min_entry.pack(side=LEFT, padx=10)
        self.max_entry = Entry(self, textvariable=self.hVar2, width=5)
        self.max_entry.pack(side=RIGHT, padx=10)
        self.rs = RangeSliderH(self, [self.hVar1, self.hVar2], min_val=min_val, max_val=max_val, Width=200, padX=20, bgColor="#D70755", line_s_color="#fff", bar_color_inner="#fff", bar_color_outer="#D70755", line_color="#FF7256",font_family="Montserrat")

        self.rs.pack(pady=10)






    def get_range(self):
        return [self.hVar1.get(), self.hVar2.get()]

    def set_range(self, range):
        self.range = range
        self.hVar1.set(range[0])
        self.hVar2.set(range[1])
        self.rs.update_range()

    def reset_range(self):
        self.set_range([self.min_val, self.max_val])

class PhotoViewer:
    def __init__(self, master):



        # Définition des options d'algorithme
        algorithm_options = {
            "Average Hashing (aHash)": "ahash",
            "Median Hashing (mHash)": "mhash",
            "Perceptual Hashing (pHash)": "phash",
            "Difference Hashing (dHash)": "dhash",
            "Block Hashing (bHash)": "bhash",
            "Wavelet Hashing (wHash)": "whash",
            "ColorMoment Hashing": "cmhash"
        }

        # Fonction appelée lorsqu'une option est sélectionnée
        def select_algorithm(event):
            selected_algorithm = algorithm_options[combo.get()]
            print("L'algorithme sélectionné est :", selected_algorithm)


        
        self.master = master
        self.master.state('zoomed') # Set window to maximum size
        self.master.title("Photo Sorting Wizard")

        # Sidebar
        self.sidebar = Frame(root, width=320, height=root.winfo_screenheight())
        self.sidebar.config(bg='#D70755')
        self.sidebar.pack_propagate(0)  # empêche le conteneur de s'adapter à son contenu
        self.sidebar.pack(side=RIGHT, fill=Y)

        # Création du label "Luminosity"
        self.labelLum = Label(self.sidebar, text="Luminosity")
        self.labelLum.config(bg='#D70755', fg='white', font=('Arial', 16, 'bold'), padx=10, pady=10, anchor='w')
        self.labelLum.pack(fill=X)

        luminosity_frame = Frame(self.sidebar, bg='#D70755')
        luminosity_frame.pack(fill=X, padx=10, pady=0)

        # self.entryLumMin = Entry(luminosity_frame)
        # self.entryLumMin.pack(side=LEFT, fill=X, padx=10, pady=0)

        # self.entryLumMax = Entry(luminosity_frame)
        # self.entryLumMax.pack(side=LEFT, fill=X, padx=10, pady=0)

        self.range_slider = RangeSliderWidget(self.sidebar, min_val=0, max_val=100, initial_range=[20, 80])
        self.range_slider.pack()

        # Création du label "BLur"
        self.labelBlur = Label(self.sidebar, text="Blur (Laplacian Variance)")
        self.labelBlur.config(bg='#D70755', fg='white', font=('Arial', 16, 'bold'), padx=10, pady=10, anchor='w')
        self.labelBlur.pack(fill=X)

        blur_frame = Frame(self.sidebar, bg='#D70755')
        blur_frame.pack(fill=X, padx=10, pady=0)

        self.entryBlurMin = Entry(blur_frame)
        self.entryBlurMin.pack(side=LEFT, fill=X, padx=10, pady=0)


        # Création du label "BLur"
        self.labelHash = Label(self.sidebar, text="HashMethod (Duplicates)")
        self.labelHash.config(bg='#D70755', fg='white', font=('Arial', 16, 'bold'), padx=10, pady=10, anchor='w')
        self.labelHash.pack(fill=X)

        # Création de la Combobox
        hash_frame = Frame(self.sidebar, bg='#D70755')
        hash_frame.pack(fill=X, padx=10, pady=0)

        self.combo = ttk.Combobox(hash_frame, values=list(algorithm_options.keys()), state="readonly")
        self.combo.set("Average Hashing (aHash)")
        self.combo.bind("<<ComboboxSelected>>", select_algorithm)
        self.combo.pack(side=LEFT)

        # Création de la case à cocher
        self.check_disable_combobox = IntVar(value=0)
        self.check_disable_combobox_checkbox = Checkbutton(hash_frame, variable=self.check_disable_combobox, bg='#D70755', fg='white', font=('Arial', 14, 'bold'), pady=10)
        self.check_disable_combobox_checkbox.pack(side=LEFT, padx=10, pady=0)


        self.folder_path = StringVar()
        self.image_paths = []
        self.current_index = 0

        # Menubar
        self.menubar = Menu(master)
        self.master.config(menu=self.menubar)

        # File menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open Folder", command=self.select_folder)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # View menu
        self.view_menu = Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label="<< Prev", command=self.show_prev_image)
        self.view_menu.add_command(label="Next >>", command=self.show_next_image)
        self.menubar.add_cascade(label="View", menu=self.view_menu)

        # Help menu
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # # Folder selection
        # self.folder_label = Label(master, text="Select a folder:")
        # self.folder_label.pack()
        # self.folder_entry = Entry(master, textvariable=self.folder_path)
        # self.folder_entry.pack()
        # self.browse_button = Button(master, text="Browse", command=self.select_folder)
        # self.browse_button.pack()

        # Image display
        self.image_label = Label(master)
        self.image_label.pack()

        # Thumbnail gallery
        self.gallery_canvas = Canvas(master, height=100)
        self.gallery_frame = Frame(self.gallery_canvas)
        self.gallery_scrollbar = Scrollbar(master, orient="horizontal", command=self.gallery_canvas.xview)
        self.gallery_canvas.configure(xscrollcommand=self.gallery_scrollbar.set)

        self.gallery_canvas.pack(side=BOTTOM, fill=X)
        self.gallery_scrollbar.pack(side=BOTTOM, fill=X)
        self.gallery_canvas.create_window((0, 0), window=self.gallery_frame, anchor=NW)

        self.gallery_frame.bind("<Configure>", lambda event, canvas=self.gallery_canvas: self.on_frame_configure(canvas))

        # Navigation buttons
        self.prev_button = Button(master, text="<< Prev", command=self.show_prev_image)
        self.prev_button.pack(side=LEFT)
        self.next_button = Button(master, text="Next >>", command=self.show_next_image)
        self.next_button.pack(side=RIGHT)



    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path.set(folder_path)
        self.load_images()

    def load_images(self):
        self.image_paths = []
        for filename in os.listdir(self.folder_path.get()):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.image_paths.append(os.path.join(self.folder_path.get(), filename))
        self.current_index = 0
        self.show_image()
        self.show_gallery()
        

    def show_gallery(self):
        # Remove existing thumbnails
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()

        # Add new thumbnails
        for i, image_path in enumerate(self.image_paths):
            thumbnail_size = (140, 140)
            image = Image.open(image_path)
            image.thumbnail(thumbnail_size)
            photo = ImageTk.PhotoImage(image)
            thumbnail_button = Button(self.gallery_frame, image=photo, command=lambda i=i: self.show_image_by_index(i))
            thumbnail_button.image = photo
            thumbnail_button.pack(side=LEFT)

        # Update scrollbar
        self.gallery_frame.update_idletasks()
        self.gallery_canvas.config(scrollregion=self.gallery_canvas.bbox("all"))

    def show_image_by_index(self, index):
        if index >= 0 and index < len(self.image_paths):
            self.current_index = index
            self.show_image()

    def show_image(self):
        if self.image_paths:
            image_path = self.image_paths[self.current_index]
            image = Image.open(image_path)
            image.thumbnail((720, 720))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image()

    def show_prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def show_about(self):
        messagebox.showinfo("About", "Photo Sorting Wizard v1.0\n\n© 2023 Yoann PETIT.")




root = Tk()
photo_viewer = PhotoViewer(root)
root.mainloop()

