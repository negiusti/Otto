// some port audio sample code used from https://github.com/albertz/music-player

#include <stdio.h>
#include <string.h>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h> 
#include <string.h>  
#include <sys/stat.h>
#include <fcntl.h>
#include <queue>
#include "portaudio.h"

#define BUFMAX 100
#define SONGS_LOCATION "./songs/"
#define SCHEDULER "python scheduler.py"

#define CHECK(x) { if(!(x)) { \
fprintf(stderr, "%s:%i: failure at: %s\n", __FILE__, __LINE__, #x); \
_exit(1); } }

PaStream* stream;
FILE* wavfile;
int numChannels;
int sampleRate;
PaSampleFormat sampleFormat;
int bytesPerSample, bitsPerSample;

std::queue<char*> songQueue;

int paStreamCallback(
	const void *input, void *output,
	unsigned long frameCount,
	const PaStreamCallbackTimeInfo* timeInfo,
	PaStreamCallbackFlags statusFlags,
	void *userData )
{
	size_t numRead = fread(output, bytesPerSample * numChannels, frameCount, wavfile);
	output = (uint8_t*)output + numRead * numChannels * bytesPerSample;
	frameCount -= numRead;
	
	if(frameCount > 0) {
		memset(output, 0, frameCount * numChannels * bytesPerSample);
		return paComplete;
	}
	
	return paContinue;
}

bool portAudioOpen() {
	CHECK(Pa_Initialize() == paNoError);
	PaStreamParameters outputParameters;

	outputParameters.device = Pa_GetDefaultOutputDevice();
	CHECK(outputParameters.device != paNoDevice);
	
	outputParameters.channelCount = numChannels;
	outputParameters.sampleFormat = sampleFormat;
	outputParameters.suggestedLatency = Pa_GetDeviceInfo( outputParameters.device )->defaultHighOutputLatency;
	
	PaError ret = Pa_OpenStream(
		&stream,
		NULL, 
		&outputParameters,
		sampleRate,
		paFramesPerBufferUnspecified,
		0,
		&paStreamCallback,
		NULL
		);
	
	if(ret != paNoError) {
		fprintf(stderr, "Pa_OpenStream failed: (err %i) %s\n", ret, Pa_GetErrorText(ret));
		if(stream)
			Pa_CloseStream(stream);
		return false;
	}
	
	CHECK(Pa_StartStream(stream) == paNoError);
	return true;
}

std::string freadStr(FILE* f, size_t len) {
	std::string s(len, '\0');
	CHECK(fread(&s[0], 1, len, f) == len);
	return s;
}

template<typename T>
T freadNum(FILE* f) {
	T value;
	CHECK(fread(&value, sizeof(value), 1, f) == 1);
	return value;
}

void readFmtChunk(uint32_t chunkLen) {
	CHECK(chunkLen >= 16);
	uint16_t fmttag = freadNum<uint16_t>(wavfile);
	CHECK(fmttag == 1 || fmttag == 3);
	numChannels = freadNum<uint16_t>(wavfile);
	CHECK(numChannels > 0);
	sampleRate = freadNum<uint32_t>(wavfile);
	uint32_t byteRate = freadNum<uint32_t>(wavfile);
	uint16_t blockAlign = freadNum<uint16_t>(wavfile);
	bitsPerSample = freadNum<uint16_t>(wavfile);
	bytesPerSample = bitsPerSample / 8;
	CHECK(byteRate == sampleRate * numChannels * bytesPerSample);
	CHECK(blockAlign == numChannels * bytesPerSample);
	if(fmttag == 1) {
		switch(bitsPerSample) {
			case 8: sampleFormat = paInt8; break;
			case 16: sampleFormat = paInt16; break;
			case 32: sampleFormat = paInt32; break;
			default: CHECK(false);
		}
	} else {
		CHECK(fmttag == 3);
		CHECK(bitsPerSample == 32);
		sampleFormat = paFloat32;
	}
	if(chunkLen > 16) {
		uint16_t extendedSize = freadNum<uint16_t>(wavfile);
		CHECK(chunkLen == 18 + extendedSize);
		fseek(wavfile, extendedSize, SEEK_CUR);
	}
}

void playSound( char *filename ) { 
	char command[256]; 
	int status;  
	char longerfilename[100];
	strcpy(longerfilename, SONGS_LOCATION);
	strcat(longerfilename, filename);
	wavfile = fopen(longerfilename, "r");
	CHECK(wavfile >= 0);

	CHECK(freadStr(wavfile, 4) == "RIFF");
	uint32_t wavechunksize = freadNum<uint32_t>(wavfile);
	CHECK(freadStr(wavfile, 4) == "WAVE");
	while(true) {
		std::string chunkName = freadStr(wavfile, 4);
		uint32_t chunkLen = freadNum<uint32_t>(wavfile);
		if(chunkName == "fmt ")
			readFmtChunk(chunkLen);
		else if(chunkName == "data") {
			CHECK(sampleRate != 0);
			CHECK(numChannels > 0);
			CHECK(bytesPerSample > 0);
			break;
		} else {
			// skip chunk
			CHECK(fseek(wavfile, chunkLen, SEEK_CUR) == 0);
		}
	}
	
	CHECK(portAudioOpen());
	
	// wait until stream has finished playing
	while(Pa_IsStreamActive(stream) > 0)
		usleep(1000);
	
	fclose(wavfile);
	Pa_CloseStream(stream);
	Pa_Terminate();
}

void getMoreSongs (char* testInput) {
	FILE *output;

	char* songInfo = (char*)malloc(10000); 
	char* songList = (char*)malloc(10000); 

	if (testInput != NULL) {
		songList = testInput;
	}
	else {
		output = popen(SCHEDULER, "r");
		while(fgets(songInfo, sizeof(songInfo), output)!=NULL){
	        strcat(songList, songInfo);
	    }
	    pclose(output); 
	}
    
	char ** res  = NULL;
	char *  p    = strtok (songList, "|");
	int n_spaces = 0, i;

	while (p) {
  		res = (char**)realloc (res, sizeof (char*) * ++n_spaces);

  		if (res == NULL)
    		exit (-1); 

  		res[n_spaces-1] = p;

  		p = strtok (NULL, "|");
	}

	res = (char**)realloc (res, sizeof (char*) * (n_spaces+1));
	res[n_spaces-1] = 0;

	i = 0;
	while (res[i] != NULL) {
		songQueue.push(res[i++]);
	}
	free(songInfo);
}

int main(int argc, char** argv) {
	char* artist;
	char* song;
	char* duration;
	char* testingSongsList = NULL;
	bool doNotPlay = false;

	if (argc > 1 && strcmp(argv[1], "-s") == 0) {
		doNotPlay = true;
		testingSongsList = argv[2];
	}
	else if (argc > 1 && strcmp(argv[1], "-p") == 0) {
		doNotPlay = false;
		testingSongsList = argv[2];
	}
	getMoreSongs(testingSongsList);

	while(!songQueue.empty()) {
		if (testingSongsList == NULL && songQueue.size() <= 6) {
			getMoreSongs(NULL);
		}
		artist = songQueue.front();
		songQueue.pop();
		song = songQueue.front();
		songQueue.pop();
		duration = songQueue.front();
		songQueue.pop();
		printf("%s %s %s\n", artist, song, duration);
		fflush(stdout);
    	if (!doNotPlay) {
			playSound(song);
		}
	}	
	return 0;
}
