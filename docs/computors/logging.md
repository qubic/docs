# Logging (Draft)

## Startup Information

<pre>
230726121457 A- 000:000(000).0.0 <span style={{backgroundColor: 'var(--code-highlighter-yellow)'}}>Qubic 1.156.0</span> is launched.{'\n'}
230726121457 A- 000:000(000).0.0 Theoretical TSC frequency = n/a.{'\n'}
230726121457 A- 000:000(000).0.0 Practical TSC frequency = 4'192'091'411 Hz.{'\n'}
230726121457 A- 000:000(000).0.0 Volume #0 (): 13'946'601'472 / 21'464'301'568 free bytes | Read-Write.{'\n'}
230726121457 A- 000:000(000).7100000.67 1'073'741'824 bytes of the spectrum data are hashed (3'765'499 microseconds).{'\n'}
230726121457 A- 000:000(000).7100000.67 56'860'000'000'000 qus in 2'722 entities (digest = rcughairuagqwfyzgqfubfqrzvceutzjufgcdveznakqwvumjczgehdboupo).{'\n'}
230726121457 A- 000:000(000).7100000.67 Universe digest = tqoshbcixaychhxgzykrrdnhdoragtqjjrrgwvwadfghzsgyfkdtdnzfwjnk.{'\n'}
230726121457 A- 000:000(000).7100000.67 Computer digest = enqmdlcdojeyxbonwdxlkzzchsubzivlqrkbnoxbwbkkcrbnbvrjbopfkrka.{'\n'}
230726121457 A- 000:000(000).7100000.67 14/14 processors are being used.{'\n'}
230726121457 A- 000:000(000).7100000.67 Local address = 123.100.321.100:21841.{'\n'}
230726121457 A- 000:000(000).7100000.67 Routes:{'\n'}
230726121457 A- 000:000(000).7100000.67 Address = 123.100.321.50 | mask = 255.255.255.192 | gateway = 0.0.0.0.{'\n'}
230726121457 A- 000:000(000).7100000.67 Address = 0.0.0.0 | mask = 0.0.0.0 | gateway = 123.100.321.55.{'\n'}
230726121511 A- 000:000(000).7100000.67 [+0 -0 *0 /0] 0|0 0/22 Dynamic (+0 -0 ...0).{'\n'}
230726121511 A- 000:000(000).7100000.67 11 | Tick = 0.0 s | Indices = ?.{'\n'}
230726121511 A- 000:000(000).7100000.67 0/0 next tick transactions are known. 0 pending transactions.{'\n'}
230726121511 A- 000:000(000).7100000.67 0 (0) :: 0 (0) | Average processing time = ? microseconds.{'\n'}
230726121511 A- 000:000(000).7100000.67 Ticker loop duration = 0 microseconds. Latest created tick = 0.{'\n'}
230726121512 A- 000:000(000).7100000.67 [+31 -0 *6 /44] 70|14 11/28 Dynamic (+2'108 -2'336 ...0).{'\n'}
230726121512 A- 000:000(000).7100000.67 11 | Tick = 0.0 s | Indices = ?.{'\n'}
</pre>

- <span style={{backgroundColor: 'var(--code-highlighter-yellow)'}}>Current protocol version</span>

## Votes

<pre>
230726122051 B- <span style={{backgroundColor: 'var(--code-highlighter-green)'}}>000</span>:<span style={{backgroundColor: 'var(--code-highlighter-red)'}}>000</span>(<span style={{backgroundColor: 'var(--code-highlighter-blue)'}}>000</span>).7100027.67 0/0 next tick transactions are known. 59 pending transactions.{'\n'}
</pre>

- <span style={{backgroundColor: 'var(--code-highlighter-green)'}}>Aligned Votes (votes on the left)</span>: These computors have the same data for the tick and are potentially aligned with tick leaders view. To proceed to next tick quorum (451+) must be aligned.
- <span style={{backgroundColor: 'var(--code-highlighter-red)'}}>Misaligned votes (votes on the right)</span>: computors can have different view, meaning they are misaligned if they do not agree with majority.
- <span style={{backgroundColor: 'var(--code-highlighter-blue)'}}>Computors ahead of your computor</span> 


## Connections
<pre>
230726122052 B- 000:000(000).7100027.67 [+26 -0 *129 /38] <span style={{backgroundColor: 'var(--code-highlighter-yellow)'}}>52</span>|<span style={{backgroundColor: 'var(--code-highlighter-red)'}}>12</span> 30/39 Dynamic (+44'252 -145'608 ...129'180).{'\n'}
230726122052 B- 000:000(000).7100027.67 11 | Tick = 7.4 s | Indices = AX[in 24 ticks]+BS[45]+DE[83].{'\n'}
</pre>

- <span style={{backgroundColor: 'var(--code-highlighter-yellow)'}}>Not connected slots</span>
- <span style={{backgroundColor: 'var(--code-highlighter-red)'}}>Connected slots</span>

Default config is 64 connections overall (60 incoming, 4 outgoing). 

## Tick durations
<pre>
230726122051 B- 000:000(000).7100027.67 0 (0) :: 0 (0) | Average processing time = 87 microseconds.{'\n'}
230726122051 B- 000:000(000).7100027.67 Ticker loop duration = 4 microseconds. Latest created tick = 7'100'026.{'\n'}
</pre>

## To be continued...

<pre>
230726122059 B- 000:000(000).7100028.67 0 (0) :: 0 (0) | Average processing time = 85 microseconds.{'\n'}
230726122059 B- 000:000(000).7100028.67 Ticker loop duration = 4 microseconds. Latest created tick = 7'100'027.{'\n'}
230726122100 D4'202'496+ 359:000(000).7100028.67 [+371 -0 *1'071 /3'443] 51|33 30/39 Dynamic (+491'316 -644'428 ...398'808).{'\n'}
230726122100 D4'202'496+ 359:000(000).7100028.67 11 | Tick = 7.4 s | Indices = AX[in 23 ticks]+BS[44]+DE[82].{'\n'}
230726122100 D4'202'496+ 359:000(000).7100028.67 0/0 next tick transactions are known. 61 pending transactions.{'\n'}
230726122100 D4'202'496+ 359:000(000).7100028.67 0 (0) :: 0 (0) | Average processing time = 84 microseconds.{'\n'}
230726122100 D4'202'496+ 359:000(000).7100028.67 Ticker loop duration = 9 microseconds. Latest created tick = 7'100'028.{'\n'}
230726122101 B- 000:000(000).7100029.67 [+160 -0 *1'034 /903] 50|34 30/39 Dynamic (+392'912 -480'164 ...216'164).{'\n'}
</pre>

<pre>
230726122217 C- 000:000(000).7100042.67 [+485 -0 *2'545 /4'519] 46|38 30/38 Dynamic (+1'033'796 -1'309'196 ...246'604).{'\n'}
230726122217 C- 000:000(000).7100042.67 11 | Tick = 5.8 s | Indices = AX[in 9 ticks].{'\n'}
230726122217 C- 000:000(000).7100042.67 ?/? next tick transactions are known. (23.07.26 12:22:13.) 38 pending transactions.{'\n'}
</pre>