import pandas as pd
from datetime import datetime
from loguru import logger
import MetaTrader5 as mt5


def login_to_mt5(account, password, server):
    mt5.initialize()
    authorized = mt5.login(account, password=password, server=server)

    return authorized


def get_account_info(account, password, server):
    try:
        # Logging in to MetaTrader 5
        authorized = login_to_mt5(account, password, server)

        if authorized:
            # Getting account information
            account_info_dict = mt5.account_info()._asdict()
            account_info_df = pd.DataFrame(account_info_dict, index=[0])
            name = account_info_df["name"].iloc[0]

            logger.info(f"Acoount Name: {name}")

            return account_info_df
        else:
            raise Exception("Login failed.")
    except Exception as e:
        logger.error(f"Error while getting account information: {str(e)}")
        raise e


def get_history_orders(account, password, server, from_date, to_date):
    try:
        mt5.initialize()
        authorized = mt5.login(account, password=password, server=server)

        history_data = mt5.history_orders_get(from_date, to_date)
        history_orders_df = pd.DataFrame(
            list(history_data), columns=history_data[0]._asdict().keys()
        )

        # Log the length of the DataFrame
        logger.info(f"Length of history_orders_df: {len(history_orders_df)}")

        return history_orders_df
    except Exception as e:
        logger.error(f"Error while getting history orders: {str(e)}")
        raise e


def get_history_deals(account, password, server, from_date, to_date):
    try:
        mt5.initialize()
        authorized = mt5.login(account, password=password, server=server)

        history_deals = mt5.history_deals_get(from_date, to_date)
        history_deals_df = pd.DataFrame(
            list(history_deals), columns=history_deals[0]._asdict().keys()
        )

        # Log the length of the DataFrame
        logger.info(f"Length of history_deals_df: {len(history_deals_df)}")

        return history_deals_df
    except Exception as e:
        logger.error(f"Error while getting history deals: {str(e)}")
        raise e


def calculate_metrics(account_size, stage):
    # Calculate additional metrics based on the provided conditions
    if 3000 <= account_size <= 50000 and stage == "Single Stage":
        profit_target_stage1 = 0.06
        profit_target_stage2 = None
        max_loss = 0.06
        daily_loss = 0.02
    elif 2000 <= account_size <= 20000 and stage == "Two Stage":
        profit_target_stage1 = 0.10
        profit_target_stage2 = 0.05
        max_loss = 0.12
        daily_loss = 0.05
    elif 2000 <= account_size <= 20000 and stage == "Rocket Stage":
        profit_target_stage1 = 0.10
        profit_target_stage2 = 0.05  # Different from stage 1 for two-stage
        max_loss = 0.05
        daily_loss = None  # No daily loss for the Rocket Stage
    else:
        raise ValueError("Invalid account size")

    return profit_target_stage1, profit_target_stage2, max_loss, daily_loss


def determine_status(
    profit_target_stage1,
    profit_target_stage2,
    max_loss,
    daily_loss,
    trading_days,
    stage,
    percentage_of_losses,
    percentage_of_profits,
    percentage_of_daily_loss,
):
    # Determine status based on the stage
    red_causes = []

    if stage == "Single Stage":
        if not (
            
            trading_days >= 3
            and percentage_of_losses >= 0.06 
            and percentage_of_profits >= 0.06 
            and percentage_of_daily_loss >= 0.02 
        ):
            red_causes.append(
                {
                    "Condition": "Single Stage",
                    "Max Loss": max_loss,
                    "Profit Target Stage 1": profit_target_stage1,
                    "Percentage of Losses": percentage_of_losses,
                    "Percentage of Profits": percentage_of_profits,
                    "Percentage of Daily Loss": percentage_of_daily_loss,
                }
            )
    elif stage == "Two Stage":
        if not (
            trading_days >= 3
            and percentage_of_losses >= 0.12  
            and percentage_of_profits >= 0.1 
            and percentage_of_daily_loss >= 0.05  
        ):
            red_causes.append(
                {
                    "Condition": "Two Stage",
                    "Max Loss": max_loss,
                    "Profit Target Stage 1": profit_target_stage1,
                    "Profit Target Stage 2": profit_target_stage2,
                    "Percentage of Losses": percentage_of_losses,
                    "Percentage of Profits": percentage_of_profits,
                    "Percentage of Daily Loss": percentage_of_daily_loss,
                }
            )
    elif stage == "Rocket Stage":
        if not (
            trading_days >= 3
            and percentage_of_losses >= 0.05
            and percentage_of_profits >= 0.1  
        ):
            red_causes.append(
                {
                    "Condition": "Rocket Stage",
                    "Percentage of Losses": percentage_of_losses,
                    "Percentage of Profits": percentage_of_profits,
                    "Percentage of Daily Loss": percentage_of_daily_loss,
                }
            )
    else:
        red_causes.append({"Condition": "N/A"})

    return "Red" if red_causes else "Green", red_causes


def generate_final_data(account_info_df, deals_dataframe, trading_days, stage):
    # Extracting relevant information from 'deals_dataframe'
    start_date = deals_dataframe["time"].iloc[0]
    number_of_trades = len(deals_dataframe)
    win_rate = (
        ((deals_dataframe["profit"] > 0).sum() / number_of_trades)
        if number_of_trades > 0
        else 0
    )
    average_win = deals_dataframe[deals_dataframe["profit"] > 0]["profit"].mean()
    average_loss = deals_dataframe[deals_dataframe["profit"] < 0]["profit"].mean()

    # Calculate absolute values of losses and profits
    absolute_losses = -deals_dataframe[deals_dataframe["profit"] < 0]["profit"].sum()
    absolute_profits = deals_dataframe[deals_dataframe["profit"] > 0]["profit"].sum()

    # Calculate percentages
    percentage_of_losses = (absolute_losses / account_info_df["equity"].iloc[0]) * 100
    percentage_of_profits = (absolute_profits / account_info_df["equity"].iloc[0]) * 100

    # Calculate percentage of average win and average loss
    percentage_of_average_win = (average_win / account_info_df["equity"].iloc[0]) * 100
    percentage_of_average_loss = (
        abs(average_loss) / account_info_df["equity"].iloc[0]
    ) * 100

    # Convert "time" column to datetime
    deals_dataframe["time"] = pd.to_datetime(deals_dataframe["time"], unit="s")

    # Calculate time difference for daily loss percentage
    daily_loss_time_diff = (
        deals_dataframe["time"].iloc[-1].replace(hour=23, minute=59, second=59)
        - deals_dataframe["time"].iloc[0].replace(hour=0, minute=0, second=0)
    ).days + 1  # Add 1 to include the last day

    # Calculate daily loss percentage
    percentage_of_daily_loss = (
        ((absolute_losses / account_info_df["equity"].iloc[0]) / daily_loss_time_diff)
        * 100
        if daily_loss_time_diff > 0
        else None
    )
    # Calculating additional metrics based on account size
    account_size = account_info_df["balance"].iloc[0]
    (
        profit_target_stage1,
        profit_target_stage2,
        max_loss,
        daily_loss,
    ) = calculate_metrics(account_size, stage)

    status, red_causes = determine_status(
        profit_target_stage1,
        profit_target_stage2,
        max_loss,
        daily_loss,
        trading_days,
        stage,
        percentage_of_losses,
        percentage_of_profits,
        percentage_of_daily_loss,
    )
    logger.info(f"Red Causes: {red_causes}")
    # Creating the final dataframe

    financial_data = pd.DataFrame(
        {
            "Start Date": [start_date],
            "Account Size": [account_size],
            "Equity": [account_info_df["equity"].iloc[0]],
            "Status": [status],
            "Profit Target": [
                f"{format(profit_target_stage1 * 100, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
                if stage != "Rocket Stage"
                else f"{format(profit_target_stage2 * 100, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
            ],
            "Daily Loss": [
                f"{format(daily_loss * 100, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
                if daily_loss is not None
                else "N/A"
            ],
            "Maximum Loss": [
                f"{format(max_loss * 100, '.2f').rstrip('0').rstrip('.')}%".lstrip("0")
            ],
            "Absolute Losses": [absolute_losses],
            "Percentage of Losses": [
                f"{format(percentage_of_losses, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
            ],
            "Absolute Profits": [absolute_profits],
            "Percentage of Profits": [
                f"{format(percentage_of_profits, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
            ],
            "Percentage of Average Win": [
                f"{format(percentage_of_average_win, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
            ],
            "Percentage of Average Loss": [
                f"{format(percentage_of_average_loss, '.2f').rstrip('0').rstrip('.')}%".lstrip(
                    "0"
                )
            ],
            "Daily Loss Time Difference (days)": [daily_loss_time_diff],
            "Active Trading Days": [trading_days],
            "Number of Trades": [number_of_trades],
            "Winrate": [win_rate],
            "Average Win": [average_win],
            "Average Loss": [average_loss],
            "Platform": ["MetaTrader 5"],  # You can change this based on your platform
            "Server": [account_info_df["server"].iloc[0]],
        }
    )

    return financial_data


def main():
    account = 51913983
    password = "drbj2iln"
    server = "Alpari-MT5-Demo"

    from_date = datetime(2023, 1, 1)
    to_date = datetime.now()

    # Get data
    login_result = login_to_mt5(account, password, server)
    if login_result:
        account_info_df = get_account_info(account, password, server)
        history_orders_df = get_history_orders(
            account, password, server, from_date, to_date
        )
        history_deals_df = get_history_deals(
            account, password, server, from_date, to_date
        )

        history_deals_df["time"] = pd.to_datetime(history_deals_df["time"], unit="s")

        # Determine the number of active trading days
        trading_days = len(history_deals_df["time"].dt.date.unique())

        # Ask the user to choose the stage
        print("Choose the analysis stage:")
        print("1. Single Stage")
        print("2. Two Stage")
        print("3. Rocket Stage")
        user_choice = int(input("Enter the number corresponding to your choice: "))

        # Process and analyze data
        if user_choice == 1:
            stage = "Single Stage"
        elif user_choice == 2:
            stage = "Two Stage"
        elif user_choice == 3:
            stage = "Rocket Stage"
        else:
            stage = "Invalid Choice"

        if stage != "Invalid Choice":
            financial_data = generate_final_data(
                account_info_df, history_deals_df, trading_days, stage
            )
            # Display the final data
            logger.info(financial_data)
        else:
            logger.info("Invalid choice. Please choose a valid analysis stage.")
    else:
        logger.info("Login failed.")


if __name__ == "__main__":
    main()
