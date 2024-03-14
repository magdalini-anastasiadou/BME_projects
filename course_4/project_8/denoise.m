function y = denoise(x,Fs)
    y = detrend(x);
 
    fc = 0.5;
    Wn = fc/(Fs/2);
    [b,a] = cheby2(6, 50, Wn, 'high');
    high_passed_signal = filtfilt(b, a, y);

    fc = 50;
    Wn = fc/(Fs/2);
    [b, a] = cheby2(6, 50, Wn, 'low');
    y = filtfilt(b, a, high_passed_signal);
    y = (y - mean(y))./std(y);
end