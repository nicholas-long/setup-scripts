```bash
┌──(coyote$kalifast)-[~/testing/setup-scripts]
└─$ echo -e 'blob 14\0Hello, World!' | shasum
8ab686eafeb1f44702738c8b0f24f2567c36da6d  -


┌──(coyote$kalifast)-[~/testing/setup-scripts]
└─$ echo -e 'Hello, World!' | git hash-object --stdin 
8ab686eafeb1f44702738c8b0f24f2567c36da6d

```