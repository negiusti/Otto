#include <stdlib.h> 
#include <stdio.h> 
#include <string.h>  
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>

#define BUFMAX 100

struct Node {
	char* data;
	struct Node* next;
};

// Two glboal variables to store address of front and rear nodes. 
struct Node* front = NULL;
struct Node* rear = NULL;

int QueueSize () {
	struct Node* temp = front;
	int s = 0;
	while (temp != NULL) {
		s++;
		temp = temp->next;
	}
	return s;
}

void Enqueue(char* x) {
	struct Node* temp = 
		(struct Node*)malloc(sizeof(struct Node));
	temp->data = malloc(strlen(x)+1);
	strcpy(temp->data, x);
	//temp->data =x; 
	temp->next = NULL;
	if(front == NULL && rear == NULL){
		front = rear = temp;
		return;
	}
	rear->next = temp;
	rear = temp;
}

void Dequeue() {
	struct Node* temp = front;
	if(front == NULL) {
		printf("Queue is Empty\n");
		return;
	}
	if(front == rear) {
		front = rear = NULL;
	}
	else {
		front = front->next;
	}
	free(temp);
}

char* Front() {
	if(front == NULL) {
		printf("Queue is empty\n");
		return NULL;
	}
	return front->data;
}

void Print() {
	struct Node* temp = front;
	while(temp != NULL) {
		printf("%s ", temp->data);
		temp = temp->next;
	}
	printf("\n");
}

int playSound( char *filename ) { 
	char command[256]; 
	int status;  /* create command to execute */

	sprintf( command, "afplay \"./songs/%s\"", filename);  /* play sound */ 
	status = system( command );  
	return status; 
}

void getMoreSongs () {
	FILE *output;

	char* blah = malloc(10000); 
	
	output = popen("python scheduler.py", "r");
	char* songList = malloc(10000); 
	
	while(fgets(blah, sizeof(blah), output)!=NULL){
        strcat(songList, blah);
    }
    printf("%s", songList);  
    pclose(output); 
    

	char ** res  = NULL;
	char *  p    = strtok (songList, "|");
	int n_spaces = 0, i;


/* split string and append tokens to 'res' */

	while (p) {
  		res = realloc (res, sizeof (char*) * ++n_spaces);

  		if (res == NULL)
    		exit (-1); /* memory allocation failed */

  		res[n_spaces-1] = p;

  		p = strtok (NULL, "|");
	}

/* realloc one extra element for the last NULL */

	res = realloc (res, sizeof (char*) * (n_spaces+1));
	res[n_spaces-1] = 0;

	i = 0;
	while (res[i] != NULL) {
		//printf("%s\n", res[i]);
		Enqueue(res[i++]);
	}
	free(blah);
}

int main( int argc, char *argv[] ) { 
	char filename[] = "fifo.tmp";
	char* artist;
	char* song;
	char* duration;

	getMoreSongs();

	while(Front() != NULL) {
	    FILE * wfd = fopen(filename, "w");
	    if (wfd < 0)
	    {
	        printf("open() error");
	        return -1;
	    }
		if (QueueSize() <= 6) {
			//printf("Getting more songs");
			getMoreSongs();
		}
		printf("Current Artist: %s\n", Front());
		artist = Front();
		Dequeue();
		printf("Current Song: %s\n\n", Front());
		song = Front();
		Dequeue();
		duration = Front();
		Dequeue();
		int s_write = fprintf(wfd, "%s %s %s\n", artist, song, duration);

        if (s_write < 0)
        {
            printf("fprintf() error:");
            break;
        }
        fclose(wfd);
    	unlink(filename);
		playSound(song);
	}
	return 0; 
}
