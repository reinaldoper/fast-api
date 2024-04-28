# Models
## Este repositório contém a definição dos seguintes modelos SQLAlchemy:

- **Todos os comando necessários estão dentro do arquivo Makefile, usando a diretiva "make <parametro>"**

## AtletaModel
### Tabela: atletas
- Campos:
- pk_id: Chave primária, inteiro.
- nome: Nome do atleta, string com no máximo 50 caracteres, obrigatório.
- cpf: CPF do atleta, string com 11 caracteres, único e obrigatório.
- idade: Idade do atleta, inteiro, obrigatório.
- peso: Peso do atleta, float, obrigatório.
- altura: Altura do atleta, float, obrigatório.
- sexo: Sexo do atleta, string com 1 caractere, obrigatório.
- created_at: Data e hora de criação do registro, obrigatório.
- categoria: Relacionamento com o modelo CategoriaModel.
- categoria_id: Chave estrangeira referenciando a tabela categorias.
- centro_treinamento: Relacionamento com o modelo CentroTreinamentoModel.
- centro_treinamento_id: Chave estrangeira referenciando a tabela centros_treinamento.

## CategoriaModel
### Tabela: categorias
- Campos:
- pk_id: Chave primária, inteiro.
- nome: Nome da categoria, string com no máximo 10 caracteres, único e obrigatório.
- atleta: Relacionamento com o modelo AtletaModel.
- created_at: Data e hora de criação do registro, obrigatório.

## CentroTreinamentoModel
### Tabela: centros_treinamento
- Campos:
- pk_id: Chave primária, inteiro.
- nome: Nome do centro de treinamento, string com no máximo 10 caracteres, único e obrigatório.
- endereco: Endereço do centro de treinamento, string com no máximo 60 caracteres, obrigatório.
- proprietario: Nome do proprietário do centro de treinamento, string com no máximo 30 caracteres, obrigatório.
- atleta: Relacionamento com o modelo AtletaModel.
- created_at: Data e hora de criação do registro, obrigatório.