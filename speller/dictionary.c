// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Check if loaded successfully
bool loaded;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int h = hash(word);
    node *tmp = table[h];
    char lower_word[strlen(word)];
    strcpy(lower_word, word);
    for (int i = 0; i < strlen(word); i++)
    {
        lower_word[i] = tolower(lower_word[i]);
    }
        while (tmp != NULL)
        {
            if (strcmp(lower_word, tmp->word) == 0)
            {
                return true;
            }
            tmp = tmp->next;
        }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int i = tolower(word[0]) - 97;
    return i;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char c;
    int counter = 0;

    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    node *n = malloc(sizeof(node));
    while (fread(&c,sizeof(char), 1, file))
    {
        if (c != '\n')
        {
            n->word[counter] = c;
            counter++;
        }
        else
        {
            n->word[counter] = '\0';
            n->next = table[n->word[0] - 97];
            table[n->word[0] - 97] = n;
            n = malloc(sizeof(node));
            counter = 0;
        }
    }
    free(n);
    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (!loaded)
    {
        return 0;
    }
    int c = 0;
    for (int i = 0; i < N; i++)
    {
        node *tmp = table[i];
        while (tmp != NULL)
        {
            tmp = tmp->next;
            c++;
        }
    }
    return c;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    int i = 0;
    for (i = 0; i < N; i++)
    {
        node *n = table[i];
        while (n != NULL)
        {
            node *tmp = n->next;
            free(n);
            n = tmp;
        }
    }
    if (i == 26)
    {
        return true;
    }
    else
    {
        return false;
    }
}
