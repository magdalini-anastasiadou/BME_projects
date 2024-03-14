function HRecg = ECG2HR(xecg, window_size, signal_fs, HR_fs)
    % Denoise
    fekg = denoise(xecg, signal_fs);

    % Detect R waves in the entire ekg
    [~, qrs_i_raw, ~] = pan_tompkin(fekg, signal_fs, 0);

    N = length(xecg);
    window_samples = window_size * signal_fs;
    HRecg_length = ceil((N-1-window_samples)/(signal_fs/HR_fs));
    HRecg = zeros(1, HRecg_length);

    for i = 1:HRecg_length
        % Select the subset of R waves that are in this window
        start_index = ceil((i - 1)*signal_fs/HR_fs) + 1;
        end_index = start_index + window_samples - 1;
        subset = qrs_i_raw(qrs_i_raw >= start_index & qrs_i_raw <= end_index);
        
        % Estimate HR in the subset
        if ~isempty(subset)
            HRecg(i) = (60 * signal_fs) / mean(diff(subset));
        else
            HRecg(i) = NaN;
        end
    end
end
