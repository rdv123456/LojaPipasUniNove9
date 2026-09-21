#include <stdio.h>
#include <stdlib.h>

// Estrutura para representar os dados de um produto da loja
struct Produto {
    int id;
    char nome[50];
    float preco;
    int estoque;
};

// Funcao auxiliar para limpar o buffer do teclado e nao travar a leitura
void limparBuffer() {
    char c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// Funcao que descobre o proximo ID livre lendo o ultimo registo do ficheiro
int pegarProximoId() {
    FILE *f = fopen("produtos.txt", "r");
    if (f == NULL) {
        return 1; // Se o ficheiro ainda nao existe, comeca no ID 1
    }

    int id = 0;
    int est;
    float pr;
    char nm[50];

    // Percorre as linhas ate a ultima para saber o maior ID
    while (fscanf(f, "%d;%[^;];%f;%d\n", &id, nm, &pr, &est) != EOF) {
    }

    fclose(f);
    return id + 1; // Devolve o proximo numero sequencial
}

// 1. CREATE: Regista um novo produto no fim do ficheiro
void cadastrarProduto() {
    struct Produto p;
    p.id = pegarProximoId();

    printf("\nCadastro de Produto (ID: %d)\n", p.id);
    printf("Nome: ");
    scanf(" %[^\n]", p.nome); // Le o nome completo mesmo com espacos

    printf("Preco: ");
    scanf("%f", &p.preco);

    printf("Estoque: ");
    scanf("%d", &p.estoque);
    limparBuffer();

    // Abre o ficheiro em modo 'a' (append) para adicionar no fim
    FILE *f = fopen("produtos.txt", "a");
    if (f == NULL) {
        printf("Erro ao abrir arquivo!\n");
        return;
    }

    // Grava os dados separados por ponto e virgula
    fprintf(f, "%d;%s;%.2f;%d\n", p.id, p.nome, p.preco, p.estoque);
    fclose(f);

    printf("Produto salvo!\n");
}

// 2. READ: Le todas as linhas do ficheiro e mostra no ecra
void listarProdutos() {
    FILE *f = fopen("produtos.txt", "r");
    if (f == NULL) {
        printf("\nNenhum produto cadastrado.\n");
        return;
    }

    struct Produto p;
    printf("\n--- Lista de Produtos ---\n");

    // Le linha por linha ate encontrar o fim do ficheiro (EOF)
    while (fscanf(f, "%d;%[^;];%f;%d\n", &p.id, p.nome, &p.preco, &p.estoque) != EOF) {
        printf("ID: %d | Nome: %s | Preco: R$ %.2f | Estoque: %d\n", p.id, p.nome, p.preco, p.estoque);
    }

    fclose(f);
}

// 3. UPDATE: Copia os dados para um ficheiro temporario atualizando o item escolhido
void alterarProduto() {
    FILE *f = fopen("produtos.txt", "r");
    if (f == NULL) {
        printf("\nNao ha produtos para alterar!\n");
        return;
    }

    // Cria um ficheiro auxiliar
    FILE *temp = fopen("temp.txt", "w");
    if (temp == NULL) {
        fclose(f);
        return;
    }

    int idAlvo;
    int achou = 0;
    struct Produto p;

    printf("\nDigite o ID para alterar: ");
    scanf("%d", &idAlvo);
    limparBuffer();

    while (fscanf(f, "%d;%[^;];%f;%d\n", &p.id, p.nome, &p.preco, &p.estoque) != EOF) {
        if (p.id == idAlvo) {
            achou = 1;
            // Pede os novos valores caso seja o ID procurado
            printf("Novo nome: ");
            scanf(" %[^\n]", p.nome);
            printf("Novo preco: ");
            scanf("%f", &p.preco);
            printf("Novo estoque: ");
            scanf("%d", &p.estoque);
            limparBuffer();

            // Grava os dados novos no temporario
            fprintf(temp, "%d;%s;%.2f;%d\n", p.id, p.nome, p.preco, p.estoque);
        } else {
            // Mantem o produto que nao sofreu alteracao
            fprintf(temp, "%d;%s;%.2f;%d\n", p.id, p.nome, p.preco, p.estoque);
        }
    }

    fclose(f);
    fclose(temp);

    // Substitui o ficheiro antigo pelo atualizado
    if (achou == 1) {
        remove("produtos.txt");
        rename("temp.txt", "produtos.txt");
        printf("Produto alterado com sucesso!\n");
    } else {
        remove("temp.txt");
        printf("ID nao encontrado!\n");
    }
}

// 4. DELETE: Copia todos os produtos para o temporario, com excecao do ID a apagar
void deletarProduto() {
    FILE *f = fopen("produtos.txt", "r");
    if (f == NULL) {
        printf("\nNao ha produtos para deletar!\n");
        return;
    }

    FILE *temp = fopen("temp.txt", "w");
    if (temp == NULL) {
        fclose(f);
        return;
    }

    int idAlvo;
    int achou = 0;
    struct Produto p;

    printf("\nDigite o ID para deletar: ");
    scanf("%d", &idAlvo);
    limparBuffer();

    while (fscanf(f, "%d;%[^;];%f;%d\n", &p.id, p.nome, &p.preco, &p.estoque) != EOF) {
        if (p.id == idAlvo) {
            achou = 1; // Encontra o ID e nao o escreve no ficheiro temporario
            printf("Produto removido!\n");
        } else {
            fprintf(temp, "%d;%s;%.2f;%d\n", p.id, p.nome, p.preco, p.estoque);
        }
    }

    fclose(f);
    fclose(temp);

    // Substitui o ficheiro antigo pelo novo sem o registo apagado
    if (achou == 1) {
        remove("produtos.txt");
        rename("temp.txt", "produtos.txt");
    } else {
        remove("temp.txt");
        printf("ID nao encontrado!\n");
    }
}

// Funcao principal que desenha o menu e gere o fluxo
int main() {
    int op = 0;

    // Ciclo continua ate ser selecionada a opcao 5 (Sair)
    while (op != 5) {
        printf("\n--- LOJA DE PIPAS ---\n");
        printf("1. Cadastrar produto\n");
        printf("2. Listar produtos\n");
        printf("3. Alterar produto\n");
        printf("4. Deletar produto\n");
        printf("5. Sair\n");
        printf("Opcao: ");
        scanf("%d", &op);
        limparBuffer();

        if (op == 1) {
            cadastrarProduto();
        } else if (op == 2) {
            listarProdutos();
        } else if (op == 3) {
            alterarProduto();
        } else if (op == 4) {
            deletarProduto();
        } else if (op == 5) {
            printf("Saindo...\n");
        } else {
            printf("Opçao invalida!\n");
        }
    }
    return 0;
}