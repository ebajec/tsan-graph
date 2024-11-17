#include <pthread.h>
#include <stdio.h>

int Global;

int doBad(int a)
{
  Global += a;
  return a/2;
}

void *Thread1(void *x) {
  doBad(1);
  return NULL;
}

void *Thread2(void *x) {
  doBad(doBad(7));
  return NULL;
}

void *Thread3(void *x) {
  doBad(10);
  return NULL;
}

int main() {
  pthread_t t[3];
  pthread_create(&t[0], NULL, Thread1, NULL);
  pthread_create(&t[1], NULL, Thread2, NULL);
  pthread_create(&t[2], NULL, Thread3, NULL);
  pthread_join(t[0], NULL);
  pthread_join(t[1], NULL);
  pthread_join(t[2], NULL);
}