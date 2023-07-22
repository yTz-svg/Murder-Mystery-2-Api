import matplotlib.pyplot as plt
import io
import base64
import cloudinary
import cloudinary.uploader
import requests
import random
import discord
from discord import app_commands
import requests
import os
import asyncio
import numpy as np
from discord import Button
import datetime
from dateutil.relativedelta import relativedelta

class MyClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logado em {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        await self.tree.sync()

client = MyClient()

@client.tree.command(description="Vereficar faca mm2")
async def pesquisar(interaction: discord.Interaction, mm2:str):
    
    try:
    
        def transformar_texto(mm2):
            if '_' in mm2:
                texto_transformado = mm2.replace('_', ' ').title().replace(' ', '_')
            else:
                texto_transformado = mm2.capitalize()
            return texto_transformado

        mm2 = transformar_texto(mm2)

        cloudinary.config( 
        cloud_name = "", 
        api_key = "", 
        api_secret = "" 
        )

        response = requests.get(f'https://request.squareweb.app/brazilhangout/mm2/{mm2}').json()
        
        if 'error' not in response:
            nome = response['Nome']
            valor = response['Valor']
            value = response['Valor']
            raridade = response['Raridade']
            obtido = response['Obtido']
            origem = response['Origem']
            estabilidade = response['Estabilidade']
            demanda = response['Demanda']
            imagem = response['Imagem']
            
            
            data_atual = datetime.date.today()

            meses_antes = 5
            data_5_meses_atras = data_atual - datetime.timedelta(days=data_atual.day)
            data_5_meses_atras = data_atual - relativedelta(months=meses_antes)
            data_formatada = data_5_meses_atras.strftime("%d/%m/%Y")
            
            tempo = [1, 2, 3, 4, 5]
            valores = [random.uniform(0, valor) for _ in range(4)]
            valores.append(valor)
            plt.clf()
            plt.style.use('dark_background')
            plt.plot(tempo, valores)
            plt.text(tempo[2], valores[0], f"({data_formatada})", ha='right', va='bottom')
            plt.text(tempo[-1], valores[-1], f"Valor {value}", ha='right', va='top')
            
            plt.title(f"Grafico do item {mm2} ({value})")
            plt.xlabel('Ultimos 5 Meses')
            plt.ylabel(f'Valor do item')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            imagem_upload = cloudinary.uploader.upload(buffer, resource_type="image")

            link_imagem = imagem_upload["secure_url"]


            embed = discord.Embed(title=f'{nome}', description=f'Origem: `{origem}`\nObtido: `{obtido}`', color=discord.Colour.green())
            embed.add_field(name="Valores", value=f"\n<:trade:1111777229320503356> |Valor: {value} seers\n<:hype:1111777232264892536> | Demanda: {demanda}/10\n<:rare:1111777234219454474> | Raridade: {raridade}/10 \n `{estabilidade}`", inline=False)
            embed.set_thumbnail(url=imagem)
            embed.set_image(url='https://media.discordapp.net/attachments/1013932573493297212/1111836653720453161/void_default_bar_1.png')
            
            palavras = ['Para pesquisar no lugar de espaço use _', 'Nossa api e publica use /Docs', 'Estamos na versão BETA, atualizações em breve...', 'Em breve lançaremos uma API para Adopt Me', 'Aceitamos doações para a hospedagem']
            dica = random.choice(palavras)
            
            
            embed.set_footer(text=f'Dica: {dica}')
            
            
            button = discord.ui.Button(style=discord.ButtonStyle.green, label='Grafico')
            button2 = discord.ui.Button(style=discord.ButtonStyle.gray, label='Json')
            view = discord.ui.View()
            view.add_item(button)
            view.add_item(button2)

            async def button_callback(interaction):
                embed = discord.Embed(title='Grafico', color=discord.Colour.green())
                embed.set_image(url=link_imagem)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
            async def button_callback2(interaction):
                embed = discord.Embed(title='Json',description=f'```{response}```',color=discord.Colour.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)


            button.callback = button_callback
            button2.callback = button_callback2
            await interaction.response.send_message(embed=embed, ephemeral=False, view=view)
        else:
            embed = discord.Embed(title=f'Item {mm2} não foi encontrado.', description=f'Lamentamos informar que o item solicitado não está disponível. Verificamos em nossas fontes de dados, porém não encontramos registros correspondentes ao item {mm2}. Pedimos desculpas pelo inconveniente causado.', color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as erro:
            embed = discord.Embed(title=f'Item {mm2} foi gerado um erro.', description=f'```{erro}``` \n\nAo executar o comando, ocorreu um erro inesperado que interrompeu a execução normal do programa. Para lidar com esse erro, utilizamos o bloco except.', color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(description="Documentação sobre a api do mm2")
async def docs(interaction: discord.Interaction):
    embed = discord.Embed(title='Endpoint: https://request.squareweb.app/brazilhangout/mm2/(item)', description='1 - Para obter informações sobre um "item" específico, faça uma solicitação GET para o endpoint mencionado, substituindo "(item)" pelo nome do item desejado.\n2 - Para editar as informações do "item", faça uma solicitação PUT para o mesmo endpoint, incluindo um objeto JSON com as informações atualizadas no corpo da requisição.\n3 - A resposta conterá as informações atualizadas do "item" em formato JSON.', color=discord.Colour.green())
    embed.add_field(name="Exemplo:", value="```Ruby\nGET: https://request.squareweb.app/brazilhangout/mm2/Candy\n\nCorpo da Requisição:\n{\n Demanda: int, Estabilidade: 'str', Imagem: 'str', Nome: 'str', Obtido: 'str', Origem: 'str', Raridade: int, Valor: int\n}``` \n \n Respeite as leis e regulamentações aplicáveis ao uso da API, incluindo direitos autorais, privacidade e proteção de dados.")
    embed.set_image(url='https://media.discordapp.net/attachments/1013932573493297212/1111836653720453161/void_default_bar_1.png')
    
    palavras = ['Para pesquisar no lugar de espaço use _', 'Nossa api e publica use /Docs', 'Estamos na versão BETA, atualizações em breve...', 'Em breve lançaremos uma API para Adopt Me', 'Aceitamos doações para a hospedagem']
    dica = random.choice(palavras) 
    embed.set_footer(text=f'Dica: {dica}')
    
    
    button1 = discord.ui.Button(style=discord.ButtonStyle.green, label='Python')
    button2 = discord.ui.Button(style=discord.ButtonStyle.green, label='C#')
    button3 = discord.ui.Button(style=discord.ButtonStyle.green, label='Javascript')
    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    async def button_callback1(interaction):
            embed = discord.Embed(title='Python',description=f'```py\nimport requests\nurl = "https://request.squareweb.app/brazilhangout/mm2/(item)"\nresponse = requests.get(url)\nif response.status_code == 200:\n    data = response.json()\n    print(data)\nelse:\n    print("Ocorreu um erro na solicitação:", response.status_code)```',color=discord.Colour.dark_blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    button1.callback = button_callback1
    
    async def button_callback2(interaction):
            embed = discord.Embed(title='C#',description='```csharp\nusing System;\nusing System.Net.Http;\n\n\class Program\n{\n    static void Main()\n   {\n        using (HttpClient client = new HttpClient())\n        {\n            string url = "https://request.squareweb.app/brazilhangout/mm2/(item)";\n            HttpResponseMessage response = client.GetAsync(url).GetAwaiter().GetResult();\n            if (response.IsSuccessStatusCode)\n            {\n                string data = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();\n                Console.WriteLine(data);\n            }\n            else\n            {\n                Console.WriteLine("Ocorreu um erro na solicitação: " + response.StatusCode);\n            }\n        }\n    }\n```',color=discord.Colour.dark_blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    button1.callback = button_callback1
    
    async def button_callback3(interaction):
            embed = discord.Embed(title="Javascript", description="```js\nconst fetch = require('node-fetch');\n\nconst url = 'https://request.squareweb.app/brazilhangout/mm2/(item)';\nfetch(url)\n  .then(response => {\n    if (response.ok) {\n      return response.json();\n    } else {\n      throw new Error('Ocorreu um erro na solicitação: ' + response.status);\n    }\n  })\n  .then(data => {\n    console.log(data);\n  })\n  .catch(error => {\n    console.log(error);\n  })```", color=discord.Colour.dark_gold())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    button1.callback = button_callback1
    button2.callback = button_callback2
    button3.callback = button_callback3

    
    await interaction.response.send_message(embed=embed, ephemeral=False,view=view)
    
@client.tree.command(description="Melhores facas do Mm2")
async def rank(interaction: discord.Interaction):
    try:
        response = requests.get("https://request.squareweb.app/brazilhangout/mm2")

        if response.status_code == 200:
            data = response.json()

            valores_e_nomes = []
            for entry in data:
                if "Valor" in entry and "Nome" in entry:
                    valor = entry["Valor"]
                    nome = entry["Nome"]
                    valores_e_nomes.append((valor, nome))

            valores_e_nomes_ordenados = sorted(valores_e_nomes, key=lambda x: int(x[0]) if str(x[0]).isdigit() else float("inf"), reverse=True)

            top_10_valores_e_nomes = valores_e_nomes_ordenados[:10]
            
            resultado = "\n".join([f"{nome}, Valor: {valor}" for valor, nome in top_10_valores_e_nomes])

            embed = discord.Embed(title=f'🏆 | Rank melhores items do Mm2', description=f'{resultado}', color=discord.Colour.green())
            embed.set_thumbnail(url='https://supremevaluelist.com/media/mm2ancients/Niks_Scythe.png')
            embed.set_image(url='https://media.discordapp.net/attachments/1013932573493297212/1111836653720453161/void_default_bar_1.png')
            palavras = ['Para pesquisar no lugar de espaço use _', 'Nossa api e publica use /Docs', 'Estamos na versão BETA, atualizações em breve...', 'Em breve lançaremos uma API para Adopt Me', 'Aceitamos doações para a hospedagem']
            dica = random.choice(palavras)
            embed.set_footer(text=f'Dica: {dica}')

            await interaction.response.send_message(embed=embed, ephemeral=False)
            
        else:
            await interaction.response.send_message("Ocorreu um erro na solicitação:", response.status_code, ephemeral=True)
    except Exception as erro:
            embed = discord.Embed(title=f'Foi gerado um erro.', description=f'```{erro}``` \n\nAo executar o comando, ocorreu um erro inesperado que interrompeu a execução normal do programa. Para lidar com esse erro, utilizamos o bloco except.', color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)



statuses = [
    discord.Activity(type=discord.ActivityType.watching, name='/rank'),
    discord.Activity(type=discord.ActivityType.streaming, name='/docs'),
    discord.Activity(type=discord.ActivityType.streaming, name='/pesquisar [mm2]')
]

@client.event
async def on_ready():
    while True:
        for status in statuses:
            await client.change_presence(activity=status)
            await asyncio.sleep(8)

client.run('')
