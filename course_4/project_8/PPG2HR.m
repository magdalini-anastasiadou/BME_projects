function HRppg = PPG2HR(xppg, window_size, signal_fs, HR_fs)
    fppg = denoise(xppg, signal_fs);
    N = length(xppg);
    window_samples = window_size * signal_fs;
    HRppg_length = ceil((N-1-window_samples)/(signal_fs/HR_fs));
    HRppg = zeros(1, HRppg_length);

    locs = find_peaks_ppg(fppg, signal_fs);
    for i = 1:HRppg_length
        start_index = ceil((i - 1)*signal_fs/HR_fs) + 1;
        end_index = start_index + window_samples - 1;
        subset = locs(locs >= start_index & locs <= end_index);

        if ~isempty(subset)
            HRppg(i) = (60 * signal_fs) / mean(diff(subset));
        else
            HRppg(i) = NaN;
        end
    end
end


function locs = find_peaks_ppg(ppg, signal_fs)
    % Peak detection phase basen on the idea in DOI: https://doi.org/10.5334/jors.241
    % To find the best fit, the standard deviation between successive differences (SDSD) is minimised
    nSteps = 500;
    min_sdsd = inf;
    threshold = 0;
    threshold_step = 0.001;
    optimal_threshold = threshold;
    
    for step = 1:nSteps
        % Detect peaks with current threshold
        [peaks, ~] = findpeaks( ...
            ppg, ...
            'MINPEAKDISTANCE', round(0.2*signal_fs), ...
            'MinPeakHeight', threshold ...
        );
        if length(peaks) > 1
            intervals = diff(peaks);
            current_sdsd = std(intervals);

            % Check if this is the minimum std so far
            if current_sdsd < min_sdsd
                if (min_sdsd - current_sdsd < 1e-4)
                    break;
                end
                min_sdsd = current_sdsd;
                optimal_threshold = threshold;
            end
        end

        % Adjust
        threshold = threshold + threshold_step;
    end
    
    % Final peak detection with optimal threshold
    [~, locs] = findpeaks( ...
        ppg, ...
        'MinPeakHeight', optimal_threshold, ...
        'MINPEAKDISTANCE', round(0.2*signal_fs) ...
    );
end