clear all
close all

addpath model
addpath old
addpath samples
addpath samples/convolvedSignals
addpath samples/mp3

%% Create an room impulse response with a given t60
% https://dsp.stackexchange.com/questions/24481/initialize-a-room-impulse-response-using-reverberation-timet60
fs = 44100; % sample rate in Hz
t60 = 0.9; % reverb time in seconds
t60_name = '09';

% Detemine the length of the impulse response. It's an infinite response so
%   some truncation is neccessary. A good starting point 1.5 times the
%   t60 which will result in 90 dB of dynamic range
n = round(fs*1.5*t60);
t = (0:n-1)'/fs;  % time vector

% Initialize to white noise, gaussian distributed
h = randn(n,1);

% Calculate the decay. During the reverb time the envelope decays by 60 dB,
%   so we have exp(decay*t60) = 1e-3; We can solve to
decay = log(1e-3)/t60;

% Apply the envelope
h = h.*exp(decay.*t);
figure(1); clf
plot(t,h);
xlabel('Time in s');

%% Convolve with sample
fsHz = fs;
fileName = 'speech_rat.wav'; % lofi.mp3 | speech_org.wav | speech_rat.wav | science-teacher-lecturing.mp3

x = readAudio(fileName,fsHz);

% Cut audiofile to 2.5 s for speech_rat and 4.9 s for lofi_long if necessary
x = x(1:2.5*44100,:);

% Zero-pad speech signal
h = cat(1, h , zeros((length(x)-length(h)),1));

% Make signal from convolution of original signal (x) and impulse response (h). 
% This is done by getting X and H in the frequency domain and multiplying 
%   (which is the same as convolution in the time domain). 
H = fft(h);
X = fft(x);
Y = H .* X;

% Back to the time domain:
y = ifft(Y);

% Make sure that signal amplitude does not exceed -1 or 1 to avoid clipping
%   and distortion in audiowrite. 
y = y ./ (1.05 * max(abs(y)));

soundsc(y,fsHz);

%% Save audio file

fileName2 = "rat";
audiowrite(sprintf('samples/%s_%s.wav', fileName2, t60_name), y, fsHz)
%mp3write(y, fsHz, 16, sprintf('samples/%s_%s.mp3', fileName2, t60_name));

