function DemoHR_PPGvsECG(data_folder_name)
    % Figures are saved in results/timestamp
    set(0,'DefaultFigureVisible','off');
    fname = "bidmc_data.mat";
    full_path = fullfile(data_folder_name, fname);
    bidmc_data = load(full_path).data;
    N = length(bidmc_data); % number of patients
    HRecg = cell(N, 1);
    HRppg = cell(N, 1);

    window = 60;
    HR_fs = 4;

    dt = datetime('now');
    formatted_dt = string(dt, "yyyy-MM-dd_HH-mm-ss");
    folder_name = sprintf("results/%s", formatted_dt);
    mkdir(folder_name);
    for i=1:N
        Fs = bidmc_data(i).ekg.fs;
        ekg = bidmc_data(i).ekg.v;
        ppg = bidmc_data(i).ppg.v;
        if bidmc_data(i).ppg.fs ~= Fs
            error("PPG Fs differs from ECG Fs");
        end

        % % Plot ekg in 1st 60 sec
        t = 0:1/Fs:(length(ekg)-1)/Fs;
        fig = figure;
        plot(t(1:60*Fs), ekg(1:60*Fs));
        xlabel("Time [msec]");
        ylabel("EKG");
        title(sprintf("EKG-Patient-%d", i));
        fig_fname = fullfile(folder_name, sprintf("EKG-Patient-%d", i));
        print(fig, fig_fname, '-dpng', '-r300');
        close(fig);

        % Plot ppg in 1st 60 sec
        fig = figure;
        plot(t(1:60*Fs), ppg(1:60*Fs));
        xlabel("Time [msec]");
        ylabel("PPG");
        title(sprintf("PPG-Patient-%d", i));
        fig_fname = fullfile(folder_name, sprintf("PPG-Patient-%d", i));
        print(fig, fig_fname, '-dpng', '-r300');
        close(fig);

        % Call methods to calculate HR
        HRecg{i} = ECG2HR(ekg, window, Fs, HR_fs);
        HRppg{i} = PPG2HR(ppg, window, Fs, HR_fs);

        % Plot HR
        t = (1/HR_fs) * (0:(length(HRppg{i})-1))+window/2;
        fig = figure;
        hold on;
        plot(t, HRecg{i});
        plot(t, HRppg{i});
        legend('HR estimation with ECG', 'HR estimation with PPG');
        ylabel("HR [bpm]");
        xlabel("Time [msec]");
        title(sprintf("HR-Patient-%d", i));
        fig_fname = fullfile(folder_name, sprintf("HR-Patient-%d", i));
        print(fig, fig_fname, '-dpng', '-r300');
        close(fig);
    end
    
    mae = zeros(N, 1);
    for i=1:N
        differences = abs(HRecg{i} - HRppg{i});
        mae(i) = mean(differences);
        fig = plot_bland_altman(HRecg{i}, HRppg{i});
        fig_fname = fullfile(folder_name, sprintf("Bland-Altman-plot-Patient-%d", i));
        print(fig, fig_fname, '-dpng', '-r300');
        close(fig);
    end
    fig=figure;
    plot(mae);
    title("Mean Absolute Error (MAE)");
    xlabel("Patients");
    fig_fname = fullfile(folder_name, "MAE");
    print(fig, fig_fname, '-dpng', '-r300');
    close(fig);

    fig=figure;
    histogram(mae, 10);
    title("Histogram of Mean Absolute Error (MAE)");
    fig_fname = fullfile(folder_name, "HIST_MAE");
    print(fig, fig_fname, '-dpng', '-r300');
    close(fig);

    T = array2table([(1:N)', mae], "VariableNames", ["Patient", "Mean Absolute Error (MAE)"]);
    mae_fname = fullfile(folder_name, "mae.csv");
    writetable(T, mae_fname);
end

function fig = plot_bland_altman(measurement_1, measurement_2)
    N = size(measurement_1);
    means = (measurement_1 + measurement_2) / 2;
    differences = measurement_1 - measurement_2;
    mean_diff = mean(differences);
    std_diff = std(differences);
    upper_limit = mean_diff + 1.96 * std_diff;
    lower_limit = mean_diff - 1.96 * std_diff;
 
    fig = figure;
    scatter(means, differences);
    hold on;
    plot(means, repmat(mean_diff, N), 'r', 'LineWidth', 2);
    plot(means, repmat(upper_limit, N), 'g--', 'LineWidth', 2);
    plot(means, repmat(lower_limit, N), 'g--', 'LineWidth', 2);
    hold off;
    title('Bland-Altman Plot');
    xlabel('Mean of measurements');
    ylabel('Difference between measurements');
    legend('Differences', 'Mean Difference', 'Limits of Agreement');
end