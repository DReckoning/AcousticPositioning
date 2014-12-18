#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define PI 3.14159365

//#define FS 31971.5
#define FS 44047.9999
//#define NSAMP 128
#define NSAMP 147

#define THRESIG 20	//stationary trial 20
#define THRESYNC 8	//stationary trial 8
#define LOOKOUT NSAMP
//#define LOCKOUT 0.35*FS

typedef struct Settings
{
	int num_rocks;
	double sync_freq;
	double* rock_freqs;
	int sync_lock;
	int rock_lock;
}setting;

void Goerz(double* input, double* output, double fs, int N, double ftarg);
void WavThrGoerz(double* input, int size, double** output, double* outputp, double fs, int N, double* ftarg, double ftargp, int rocks);	
int FindTimes(double* input, int size, double* output, double thres, int lockout, int lookout, double fs);
int FindMax(double* input, int length);
setting* GetSettings(int number_rocks, double sync_f, double* rock_f, double sync_l, double rock_l);

int main(int argc, char *argv)
{
    
    
	int rocks=2;
	double sync_fr;
	double rock_fr[rocks];
	double sync_loc;
	double rock_lo;
	int k=0;
	double temp;
	sync_fr=6000;
	
	*(rock_fr)=3000;
	
	*(rock_fr+1)=4500;
	
	sync_loc= 0.75;
	rock_lo= 0.4;
	
	setting* current_setting=GetSettings(rocks, sync_fr, rock_fr, sync_loc, rock_lo);
		
	//reading in data
	FILE *fr;
	FILE *fout;
	int size;
	int j=0;
	
	fr=fopen("transfer.txt","rt");
	fscanf(fr, "%d", &size);
	double *wavdata=(double*) malloc(size*8);
	while(fscanf(fr,"%lf",wavdata+j) ==1 ){
		j++;
	}
	fclose(fr);
	
	//process data
	double *signalmags[current_setting->num_rocks];
	for(j=0;j<current_setting->num_rocks;j++){
		signalmags[j]=(double*) malloc((size-NSAMP)*8);
	}
	double *syncmag=(double*) malloc((size-NSAMP)*8);
	
	WavThrGoerz(wavdata, size, signalmags, syncmag, FS, NSAMP, current_setting->rock_freqs, current_setting->sync_freq, (current_setting->num_rocks));
	
	free(wavdata);
	
	//now for the max finder
//	double *signaltimes[current_setting->num_rocks];
//	
//	for(j=0;j<current_setting->num_rocks;j++){
//		signaltimes[j]=(double*) malloc(1024*8);;
//	}
	double signaltimes[current_setting->num_rocks][1024];
	
	double synctime[1024];
	int numsigs[current_setting->num_rocks];
	
	for (j=0;j<current_setting->num_rocks;j++){
		numsigs[j]=FindTimes(*(signalmags+j), (size-NSAMP), &(signaltimes[j][0]), THRESIG, current_setting->rock_lock, LOOKOUT, FS);
	}
	int numsyncs=FindTimes(syncmag, (size-NSAMP), synctime, THRESYNC, current_setting->sync_lock, LOOKOUT, FS);

	int i;

   fout=fopen("run3testet.txt","w");
   
   if (fout==NULL)
	{
		printf("Error Opening File!\n");
		exit(1);
	}
	for (j=0;j<current_setting->num_rocks;j++){
		for(i=0;i<numsigs[j];i++){
			fprintf(fout,"%lf, ",signaltimes[j][i]);
		}
		fprintf(fout,"\n");
	}

	for(i=0;i<numsyncs;i++){
		fprintf(fout,"%lf, ",synctime[i]);
	}
	fclose(fout);
	
	for (j=0;j<current_setting->num_rocks;j++){
		free(signalmags[j]);
	}

	free(syncmag);
	free(current_setting);
	
	return 0;
}

setting* GetSettings(int number_rocks, double sync_f, double* rock_f, double sync_l, double rock_l)
{
	setting* p=malloc(sizeof(setting));
	int i=0;
	
	p->num_rocks=number_rocks;
	p->sync_freq=sync_f;
	p->rock_freqs=rock_f;
		
	p->sync_lock=(int) (sync_l*FS);
	p->rock_lock=(int) (rock_l*FS);
	return p;
}

int FindMax(double* input, int length)
{
	double max=0;
	int indmax=0;
	
	int i;
	for(i=0;i<length;i++){
		if (input[i]>max){
			max=input[i];
			indmax=i;
		}
	}
	return indmax;
}


int FindTimes(double* input, int size, double* output, double thres, int lockout, int lookout, double fs)
{
	int x=0;
	int flag=0;
	int i;
	for(i=0;i<(size-lookout);i++){
		flag--;
		if ((input[i]>thres)&&(flag<0)){
			int hold=FindMax(input+i,lookout);
			output[x]=(double)(hold+i)/fs;
			x++;
			flag=lockout;}
		}
	x--;
	return x;
}
	
void WavThrGoerz(double* input, int size, double** output, double* outputp, double fs, int N, double* ftarg, double ftargp, int rocks){
	int i;
	int j;
	for(i=0;i<(size-N);i++){
		for (j=0; j<rocks; j++){
			Goerz(input+i, *(output+j)+i, fs, N, *(ftarg+j));
		}
		Goerz(input+i, outputp+i, fs, N, ftargp);
	}
	return;
}


void Goerz(double* input, double* output, double fs, int N, double ftarg)
{
	int k=floor(0.5+N*ftarg/fs);
	double w=(2*PI/N)*k;
	double cosine=cos(w);
	double sine=sin(w);
	double coeff=2*cosine;
	
	double Q1=0;
	double Q2=0;
	double Q0;
	
	int y;
	for(y=0;y<N;y++){
		Q0=coeff*Q1-Q2+input[y];
		Q2=Q1;
		Q1=Q0;
	}
	
	*output=Q1*Q1+Q2*Q2-Q1*Q2*coeff;
	
	return;
}
