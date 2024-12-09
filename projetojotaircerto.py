import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class Cultura:
    def __init__(self, nome, tempo_colheita, estacao, fertilizantes, sementes_por_hectare, produtividade_por_hectare):
        self.nome = nome
        self.tempo_colheita = tempo_colheita
        self.estacao = estacao
        self.fertilizantes = fertilizantes
        self.sementes_por_hectare = sementes_por_hectare
        self.produtividade_por_hectare = produtividade_por_hectare

    def calcular_data_colheita(self, data_plantio):
        try:
            dia, mes, ano = map(int, data_plantio.split('/'))
            data = datetime(ano, mes, dia) + timedelta(days=self.tempo_colheita)
            return data.strftime("%d/%m/%Y")
        except ValueError:
            return "Data inválida"

    def validar_estacao(self, data_plantio):
        try:
            dia, mes, ano = map(int, data_plantio.split('/'))
            return mes in self.estacao
        except ValueError:
            return False

    def calcular_sementes(self, hectares):
        return self.sementes_por_hectare * hectares

    def calcular_producao(self, hectares):
        return self.produtividade_por_hectare * hectares

    def obter_estacao_ideal(self):
        meses = ", ".join(map(str, self.estacao))
        return f"Estação Ideal: {meses}"

class Milho(Cultura):
    def __init__(self):
        super().__init__(
            nome="🌽 Milho",
            tempo_colheita=90,
            estacao=[12, 1, 2],
            fertilizantes={ 
                "Nitrogênio": "Ureia (200 kg/ha)",
                "Fosfato": "Superfosfato Simples (150 kg/ha)",
                "Potássio": "Cloreto de Potássio (100 kg/ha)"
            },
            sementes_por_hectare=60000,
            produtividade_por_hectare=5443  # Atualizado para 5443 kg/ha
        )

class Soja(Cultura):
    def __init__(self):
        super().__init__(
            nome="🌱 Soja",
            tempo_colheita=120,
            estacao=[3, 4, 5],
            fertilizantes={ 
                "Nitrogênio": "Não necessário",
                "Fosfato": "Superfosfato Simples (100 kg/ha)",
                "Potássio": "Cloreto de Potássio (100 kg/ha)"
            },
            sementes_por_hectare=350000,
            produtividade_por_hectare=3820  # Atualizado para 3820 kg/ha
        )

class Trigo(Cultura):
    def __init__(self):
        super().__init__(
            nome="🌾 Trigo",
            tempo_colheita=70,
            estacao=[6, 7, 8],
            fertilizantes={ 
                "Nitrogênio": "Ureia (150 kg/ha)",
                "Fosfato": "Superfosfato Simples (120 kg/ha)",
                "Potássio": "Cloreto de Potássio (90 kg/ha)"
            },
            sementes_por_hectare=2500000,
            produtividade_por_hectare=3500  # Atualizado para 3500 kg/ha
        )

class SimuladorPlantioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Plantio LV")
        self.root.geometry("800x600")
        self.root.configure(bg="#e7f4d3")
        self.culturas = {
            "🌽 Milho": Milho(),
            "🌱 Soja": Soja(),
            "🌾 Trigo": Trigo()
        }
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 14), background="#e7f4d3", foreground="#375a22")
        style.configure("TButton", font=("Arial", 12), background="#375a22", foreground="white")
        style.map("TButton", background=[("active", "#4b8c2a")])
        style.configure("TEntry", font=("Arial", 12))

        titulo = tk.Label(self.root, text="🌾 Simulador de Plantio LV🌽", font=("Arial", 24, "bold"), bg="#375a22", fg="white", pady=10)
        titulo.pack(fill=tk.X)

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Escolha a cultura para plantio:").grid(row=0, column=0, sticky="w", pady=5)
        self.cultura_var = tk.StringVar()
        cultura_menu = ttk.Combobox(frame, textvariable=self.cultura_var, values=list(self.culturas.keys()), state="readonly", font=("Arial", 12))
        cultura_menu.grid(row=0, column=1, sticky="ew", pady=5)
        cultura_menu.bind("<<ComboboxSelected>>", self.atualizar_estacao_ideal)

        ttk.Label(frame, text="Data de plantio (dd/mm/aaaa):").grid(row=1, column=0, sticky="w", pady=5)
        self.data_plantio_entry = ttk.Entry(frame)
        self.data_plantio_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Quantidade de hectares:").grid(row=2, column=0, sticky="w", pady=5)
        self.hectares_entry = ttk.Entry(frame)
        self.hectares_entry.grid(row=2, column=1, sticky="ew", pady=5)

        self.resultado_var = tk.StringVar()
        resultado_label = ttk.Label(frame, textvariable=self.resultado_var, wraplength=500)
        resultado_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.estacao_ideal_var = tk.StringVar()
        estacao_label = ttk.Label(frame, textvariable=self.estacao_ideal_var, wraplength=500)
        estacao_label.grid(row=4, column=0, columnspan=2, pady=10)

        calcular_button = ttk.Button(frame, text="Calcular", command=self.calcular_colheita)
        calcular_button.grid(row=5, column=0, columnspan=2, pady=20)

    def atualizar_estacao_ideal(self, event):
        cultura_nome = self.cultura_var.get()
        cultura = self.culturas.get(cultura_nome)
        if cultura:
            estacao_ideal = cultura.obter_estacao_ideal()
            self.estacao_ideal_var.set(estacao_ideal)

    def calcular_colheita(self):
        cultura_nome = self.cultura_var.get()
        data_plantio = self.data_plantio_entry.get()
        try:
            hectares = float(self.hectares_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade de hectares inválida.")
            return

        cultura = self.culturas.get(cultura_nome)
        if not cultura:
            messagebox.showerror("Erro", "Cultura não encontrada.")
            return

        if not cultura.validar_estacao(data_plantio):
            messagebox.showerror("Erro", "Data de plantio não corresponde à estação correta.")
            return

        data_colheita = cultura.calcular_data_colheita(data_plantio)
        sementes = cultura.calcular_sementes(hectares)
        producao = cultura.calcular_producao(hectares)
        recomendacoes = "\n".join(f"{nutriente}: {desc}" for nutriente, desc in cultura.fertilizantes.items())

        resultado = (
            f"Data de Colheita Estimada: {data_colheita}\n"
            f"Quantidade de Sementes: {sementes:,}\n"
            f"Estimativa de Produção: {producao:,.2f} kg\n\n"
            f"Recomendações de Fertilizantes:\n{recomendacoes}"
        )
        self.resultado_var.set(resultado)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorPlantioApp(root)
    root.mainloop()
