import streamlit as st
import pandas as pd
import numpy as np
import io
import datetime

# --- 1. Define Status Categories and Helpers (UNMODIFIED) ---
CONFIRMED_STATUSES = [
    "CONFIRMED VIA EMAIL - ONE TIME (FULL)", "CONFIRMED VIA CALLS - ONE TIME (FULL)",
    "CONFIRMED VIA EMAIL - EPA DEFAULTED", "CONFIRMED VIA VIBER - PERENNIAL",
    "CONFIRMED VIA EMAIL - DOWNPAYMENT FULL", "CONFIRMED VIA VIBER - EPA DOWNPAYMENT FULL",
    "CONFIRMED VIA VIBER - EPA DOWNPAYMENT", "CONFIRMED VIA EMAIL - EPA DOWNPAYMENT",
    "CONFIRMED VIA CALLS - EPA COMPLIED", "CONFIRMED VIA VIBER - EPA COMPLIED",
    "CONFIRMED VIA CALLS - PERENNIAL", "CONFIRMED VIA VIBER - ONE TIME (FULL)",
    "CONFIRMED VIA CALLS - EPA DOWNPAYMENT FULL", "CONFIRMED VIA CALLS - EPA DEFAULTED",
    "CONFIRMED VIA EMAIL - PERENNIAL", "CONFIRMED VIA EMAIL - EPA COMPLIED",
    "CONFIRMED VIA CALLS - EPA DOWNPAYMENT", "CONFIRMED VIA CALLS - EPA DOWNPAYMENT SPLIT",
    "CONFIRMED VIA VIBER - ONE TIME (SPLIT)", "CONFIRMED VIA EMAIL - EPA FULLY PAID",
    "CONFIRMED VIA VIBER - EPA DOWNPAYMENT SPLIT", "CONFIRMED VIA CALLS - ONE TIME (SPLIT)",
    "CONFIRMED VIA EMAIL - EPA PRE TERMINATION", "CONFIRMED VIA CALLS - EPA FULLY PAID",
    "CONFIRMED VIA EMAIL - ONE TIME (SPLIT)", "CONFIRMED VIA VISIT - EPA COMPLIED",
    "CONFIRMED VIA SMS - ONE TIME (SPLIT)", "CONFIRMED VIA VISIT - DOWNPAYMENT FULL",
    "CONFIRMED VIA EMAIL - EPA DOWNPAYMENT SPLIT", "CONFIRMED VIA VISIT - EPA DOWNPAYMENT SPLIT",
    "CONFIRMED SPM - PAID OB FULLY PAID", "CONFIRMED VIA VIBER - EPA DEFAULTED",
    "CONFIRMED VIA SMS - EPA COMPLIED", "CONFIRMED SPM - PERENNIAL",
    "CONFIRMED VIA SKIPS - ONE TIME (SPLIT)", "CONFIRMED VIA VISIT - EPA DEFAULTED",
    "CONFIRMED VIA VISIT - EPA DOWNPAYMENT", "CONFIRMED VIA VISIT - ONE TIME (SPLIT)",
    "CONFIRMED VIA VIBER - EPA FULLY PAID", "CONFIRMED VIA SKIPS - EPA DOWNPAYMENT SPLIT",
    "CONFIRMED VIA SMS - DOWNPAYMENT FULL", "CONFIRMED VIA VISIT - ONE TIME (FULL)",
    "CONFIRMED VIA SMS - ONE TIME (FULL)", "CONFIRMED VIA EMAIL - PERENNIAL"
]

PTP_STATUSES = [
    "PTP EPA - COMPLYING", "PTP OLD - RENEGO EPA WITH DOWNPAYMENT",
    "PTP NEW NEGO - EPA WITH DOWNPAYMENT", "PTP NEW NEGO - ONE TIME (SPLIT)",
    "PTP NEW NEGO - PERENNIAL", "PTP NEW NEGO - ONE TIME (FULL)",
    "PTP EPA - DEFAULTED", "PTP OLD - RENEGO OTP SPLIT",
    "PTP OLD - RENEGO OTP", "PTP OLD - RENEGO EPA WITHOUT DOWNPAYMENT",
    "PTP NEW NEGO - EPA NO DOWNPAYMENT", "PTP EPA - SPLIT DOWNPAYMENT",
    "PTP EPA - PRE TERMINATION", "PTP NEW NEGO - PERENNIAL",
    "PTP EPA - COMPLYING"
]

PTP_FF_STATUSES = [
    "PTP_FF UP - KEEPS ON RINGING (KOR)", "PTP_FF UP - ANSWERED RENEGO",
    "PTP_FF UP - ANSWERED WILL SETTLE", "SMS SENT - T3 PTP REMINDER",
    "PTP_FF UP - UNCONTACTABLE", "LS VIA EMAIL - T3 PTP REMINDER",
    "PTP_FF UP - BUSY"
]

RPC_STATUSES = [
    "RPC_INBOUND CALL (IC) - RETURN CALL", "RPC_REPLY FROM SOCMED - VIBER",
    "RPC_INBOUND CALL (IC) - NEGO", "RPC_REPLY FROM SOCMED - OTHER SOCMED PLAN",
    "RPC_INBOUND CALL (IC) - INQUIRY", "RPC_REPLY FROM SOCMED - FRAUD",
    "POS CLIENT - RFD UNEMPLOYED", "POS CLIENT - RFD CLAIMING WITH DISPUTE",
    "POS CLIENT - RFD CLIENT IS BREADWINNER", "POS CLIENT - RFD CLIENT IS UNDER MEDICATION",
    "POS CLIENT - RFD FRAUD VICTIM", "POS CLIENT - RFD WITH OTHER LOANS TO PAY",
    "POS CLIENT - RFD BUSINESS SLOWDOWN", "POS CLIENT - RFD OUT OF THE COUNTRY (OOTC)",
    "POS CLIENT - RFD FUNDS WAS DELAYED", "POS CLIENT - RFD CLIENT WAS SCAMMED",
    "POS CLIENT - RFD BUSINESS BANKRUPTCY", "POS CLIENT - RFD NOT RECEIVEING SOA BILLING",
    "POS CLIENT - RFD 3RD PARTY UNDER MEDICATION", "POS CLIENT - RFD VICTIM OF NATURAL CALAMITY",
    "POS CLIENT - RFD BUSINESS SLOWDOWN/BANKRUPTCY", "POS CLIENT - RFD CLAIMING FULLY PAID"
]

SMS_STATUSES = [
    "SMS SENT", "BULK SMS SENT", "SMS SENT - T7 PROMO OFFER LETTER",
    "SMS SENT - T10 PRE TERMINATION OFFER", "SMS SENT - T6 NO RESPONSE FROM SMS AND EMAIL",
    "LS VIA EMAIL - T6 NO RESPONSE (SMS & EMAIL)", "SMS SENT - T1 NOTIFICATION",
    "SMS RECEIVED - NO SUCH PERSON (NSP)", "SMS RECEIVED - WILL SETTLE",
    "SMS FAILED", "SMS SENT - T8 AMNESTY PROMO TEMPLATE",
    "SMS SENT - T9 RESTRUCTURING", "LS VIA SOCMED - T6 NO RESPONSE (SMS & EMAIL)",
    "SMS RECEIVED - TFIP", "SMS RECEIVED - UNDER NEGO",
    "SMS SENT - OTHERS", "SMS SENT - T12 THIRD PARTY TEMPLATE",
    "SMS SENT - T2 DEBT MANAGEMENT ASSISTANCE", "SMS SENT - T4 BROKEN PTP EPA", "SMS SENT - T5 BROKEN PTP SPLIT AND OTP"
]

EMAIL_STATUSES = [
    "LETTER RECEIVED - THRU EMAIL", "LS VIA EMAIL - T8 AMNESTY PROMO TEMPLATE",
    "LS VIA EMAIL - T1 NOTIFICATION", "LS VIA EMAIL - T7 PROMO OFFER LETTER",
    "LS VIA EMAIL - OTHERS", "LS VIA EMAIL - T9 RESTRUCTURING",
    "LS VIA EMAIL - T11 4MOS PAST DUE TEMPLATE", "LS VIA EMAIL - T2 DEBT MANAGEMENT ASSISTANCE",
    "LS VIA EMAIL - T12 THIRD PARTY TEMPLATE", "LETTER RECEIVED - LBC OR REGULAR MAIL",
    "LS VIA EMAIL - T4 BROKEN PTP EPA", "LS VIA EMAIL - T5 BROKEN PTP SPLIT AND OTP"
]

SOCMED_LS_STATUSES = [
    "LS VIA SOCMED - T7 PROMO OFFER LETTER", "LS VIA SOCMED - T8 AMNESTY PROMO TEMPLATE",
    "LS VIA SOCMED - T1 NOTIFICATION", "LS VIA SOCMED - T9 RESTRUCTURING",
    "LS VIA SOCMED - OTHERS"
]

POS_FIELD_STATUSES = [
    "FIELD RESULT - POS", "FIELD VISIT - VST RESULT_POS CH",
    "FIELD VISITATION - VST RESULT_POS THIRD PARTY"
]

NEG_FIELD_STATUSES = [
    "FIELD RESULT - NEG", "FIELD RESULT - LBC NEG",
    "FIELD VISIT - VST RESULT_NEG", "FIELD VISIT - INCOMPLETE ADDRESS",
    "DL REQUEST - SPECIAL VISIT"
]

CONNECTED_3RD_PARTY_STATUSES = [
    "POS 3RD PARTY - NO LONGER CONNECTED", "POS 3RD PARTY - CLIENT NOT AROUND",
    "POS 3RD PARTY - UNCOOPERATIVE", "POS 3RD PARTY - DECEASED",
    "POS 3RD PARTY - CLIENT OUT OF THE COUNTRY", "TRANSFER PRESENTATION - 3RD PARTY"
]

POS_SKIP_STATUSES = [
    "POS VIA SOCMED - FACEBOOK",
    "POS VIA SOCMED - OTHER SOCMED PLATFORMS", "POS VIA SOCMED - LINKEDIN",
    "POS VIA SOCMED - GOOGLE SEARCH"
]

NEG_SKIP_STATUSES = [
    "NEG VIA SOCMED - FACEBOOK",
    "NEG VIA SOCMED - LINKEDIN", "NEG VIA SOCMED - OTHER SOCMED PLATFORMS",
    "NEG VIA SOCMED - GOOGLE SEARCH", "NEG VIA SOCMED - INSTAGRAM"
]

POS_VIBER_STATUSES = ["POS VIA SOCMED - VIBER"]
NEG_VIBER_STATUSES = ["NEG VIA SOCMED - VIBER"]

# --- Time Conversion Helper (UNMODIFIED) ---
def seconds_to_hms(seconds):
    try:
        if seconds <= 0:
            return "0:00:00"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"
    except:
        return ""

# --- 2. Filter Extraction Function (UPDATED: Now includes Remark) ---
@st.cache_data(show_spinner=False)
def extract_filter_ics(filter_file):
    if filter_file is None:
        return None, None
    
    try:
        dtype_map = {'Old IC': str, 'Cycle': str, 'Remark': str}
        parse_dates = ['Assign Date']
        filter_df = pd.read_excel(
            filter_file,
            engine='openpyxl',
            dtype=dtype_map,
            parse_dates=parse_dates
        )
        filter_df.columns = filter_df.columns.str.strip()
        
        required_cols = ['Old IC', 'Assign Date', 'Cycle']
        if not all(col in filter_df.columns for col in required_cols):
            st.error(f"The filter file must contain all required columns: {', '.join(required_cols)}")
            return None, None
            
        filter_df.rename(columns={'Old IC': 'CH Code'}, inplace=True)
        filter_df['CH Code'] = filter_df['CH Code'].astype(str).str.strip()
        filter_df = filter_df[filter_df['CH Code'] != ''].copy()
        filter_df.drop_duplicates(subset=['CH Code'], keep='first', inplace=True)
        
        filter_df['Assign Date'] = filter_df['Assign Date'].dt.strftime('%Y-%m-%d').fillna('')
        
        # Handle Remark column safely
        if 'Remark' in filter_df.columns:
            filter_df['Remark'] = filter_df['Remark'].astype(str).str.strip()
            filter_df['Remark'] = filter_df['Remark'].replace({'nan': '', '<NA>': '', 'None': ''})
        else:
            filter_df['Remark'] = ''  # Add empty column if missing
        
        ic_filter_set = set(filter_df['CH Code'].unique())
        merge_df = filter_df[['CH Code', 'Assign Date', 'Cycle', 'Remark']]
        
        return ic_filter_set, merge_df
        
    except Exception as e:
        st.error(f"Error reading filter file: {e}")
        return None, None

# --- 3. Main Processing Function (UPDATED: Remark included in column order) ---
@st.cache_data(show_spinner=False)
def process_data(uploaded_files, ic_filter_set, merge_df):
    if not uploaded_files:
        return None, None, None
    st.info(f"Processing {len(uploaded_files)} file(s)... This may take a moment.")
    
    all_data = []
    
    for file in uploaded_files:
        try:
            df = pd.read_excel(
                file,
                engine='openpyxl',
                dtype={
                    'Old IC': str, 'Status': str, 'Remark Type': str,
                    'Remark': str, 'Balance': float, 'Claim Paid Amount': float,
                    'PTP Amount': float, 'PTP Date': str, 'Talk Time Duration': float, 
                    'Time': str
                },
                parse_dates=['Date', 'Claim Paid Date']
            )
            
            df.columns = df.columns.str.strip()
            
            required_cols = {
                'Old IC': 'CH Code', 'Status': 'Status', 'Remark Type': 'Remark Type',
                'Remark': 'Remark', 'Balance': 'Balance', 'Date': 'Date',
                'Claim Paid Amount': 'Claim Paid Amount', 'PTP Amount': 'PTP Amount',
                'PTP Date': 'PTP Date', 'Claim Paid Date': 'Claim Paid Date',
                'Talk Time Duration': 'Talk Time Duration',
                'Time': 'Time'
            }
            
            df = df[[col for col in required_cols.keys() if col in df.columns]]
            df = df.rename(columns=required_cols)
            
            df['CH Code'] = df['CH Code'].fillna('').astype(str).str.strip()
            df['Status'] = df['Status'].fillna('')
            df['Remark Type'] = df['Remark Type'].fillna('')
            df['Remark'] = df['Remark'].fillna('')
            df['Balance'] = df['Balance'].fillna(0)
            df['Claim Paid Amount'] = df['Claim Paid Amount'].fillna(0)
            df['PTP Amount'] = df['PTP Amount'].fillna(0)
            df['PTP Date'] = df['PTP Date'].fillna('')
            df['Talk Time Duration'] = pd.to_numeric(df['Talk Time Duration'], errors='coerce').fillna(0)
            df['Time'] = df['Time'].fillna('')
            
            all_data.append(df)
        except Exception as e:
            if "Missing column provided to 'parse_dates'" in str(e):
                st.error(f"Error reading file **{file.name}**: Missing required date column.")
            else:
                st.error(f"Error reading file **{file.name}**: {e}")
            return None, None, None
            
    if not all_data:
        st.warning("No data was successfully loaded from the files.")
        return None, None, None
        
    combined_df = pd.concat(all_data, ignore_index=True)
    
    if ic_filter_set:
        initial_rows = len(combined_df)
        combined_df = combined_df[combined_df['CH Code'].isin(ic_filter_set)]
        filtered_rows = len(combined_df)
        if filtered_rows == 0:
            st.warning("After applying the filter, no matching records were found.")
            return None, None, None
        else:
            st.info(f"Filtered from {initial_rows} to {filtered_rows} rows.")
    
    processed_df = combined_df.copy()
    ch_codes = processed_df['CH Code'].unique()
    summary_df = pd.DataFrame({'CH Code': ch_codes})
    
    if merge_df is not None:
        summary_df = pd.merge(summary_df, merge_df, on='CH Code', how='left')
    
    # Balance
    balance_summary = processed_df.groupby('CH Code')['Balance'].first().reset_index()
    balance_summary.rename(columns={'Balance': 'BALANCE'}, inplace=True)
    summary_df = pd.merge(summary_df, balance_summary, on='CH Code', how='left')
    
    # CONFIRMED Counts & Amount
    def calculate_status_metric(df, status_list, amount_col=None):
        mask = df['Status'].isin(status_list)
        if amount_col == 'Claim Paid Amount':
            mask &= (df['Claim Paid Amount'] > 0)
            return df[mask].groupby('CH Code')[amount_col].sum().reset_index(name='Result')
        return df[mask].groupby('CH Code').size().reset_index(name='Result')
    
    conf_counts = calculate_status_metric(processed_df, CONFIRMED_STATUSES)
    summary_df = pd.merge(summary_df, conf_counts.rename(columns={'Result': 'CONFIRMED'}), on='CH Code', how='left')
    
    # Last Confirmed Date
    confirmed_records = processed_df[
        (processed_df['Status'].isin(CONFIRMED_STATUSES)) & 
        (processed_df['Claim Paid Amount'] > 0)
    ].copy()
    last_conf_date_summary = confirmed_records.groupby('CH Code')['Claim Paid Date'].max().reset_index()
    last_conf_date_summary['Claim Paid Date'] = last_conf_date_summary['Claim Paid Date'].dt.strftime('%Y-%m-%d').fillna('')
    last_conf_date_summary.rename(columns={'Claim Paid Date': 'Last Confirmed Date'}, inplace=True)
    summary_df = pd.merge(summary_df, last_conf_date_summary, on='CH Code', how='left')
    
    conf_sum = calculate_status_metric(processed_df, CONFIRMED_STATUSES, amount_col='Claim Paid Amount')
    summary_df = pd.merge(summary_df, conf_sum.rename(columns={'Result': 'CONFIRMED ₱'}), on='CH Code', how='left')
    
    # PTP
    ptp_counts = processed_df[processed_df['Status'].isin(PTP_STATUSES)].groupby('CH Code').size().reset_index(name='PTP')
    summary_df = pd.merge(summary_df, ptp_counts, on='CH Code', how='left')
    
    ptp_records = processed_df[processed_df['Status'].isin(PTP_STATUSES)].copy()
    latest_ptp_idx = ptp_records.groupby('CH Code')['Date'].idxmax()
    latest_ptp_records = ptp_records.loc[latest_ptp_idx].copy()
    
    latest_ptp_amount_summary = latest_ptp_records[['CH Code', 'PTP Amount']].copy()
    latest_ptp_amount_summary.rename(columns={'PTP Amount': 'PTP ₱'}, inplace=True)
    summary_df = pd.merge(summary_df, latest_ptp_amount_summary, on='CH Code', how='left')
    
    latest_ptp_records['Latest PTP Date'] = latest_ptp_records.apply(
        lambda row: f"{str(row['PTP Date']).split(' ')[0]} {row['Time']}"
        if row['PTP Date'] != '' and row['Time'] != '' else row['PTP Date'],
        axis=1
    ).fillna('')
    latest_ptp_date_summary = latest_ptp_records[['CH Code', 'Latest PTP Date']].copy()
    summary_df = pd.merge(summary_df, latest_ptp_date_summary, on='CH Code', how='left')
    
    # RPC
    rpc_counts = calculate_status_metric(processed_df, RPC_STATUSES)
    summary_df = pd.merge(summary_df, rpc_counts.rename(columns={'Result': 'RPC'}), on='CH Code', how='left')
    
    rpc_records = processed_df[processed_df['Status'].isin(RPC_STATUSES)].copy()
    last_rpc_date_summary = rpc_records.groupby('CH Code')['Date'].max().reset_index()
    last_rpc_date_summary['Date'] = last_rpc_date_summary['Date'].dt.strftime('%Y-%m-%d').fillna('')
    last_rpc_date_summary.rename(columns={'Date': 'Last RPC Date'}, inplace=True)
    summary_df = pd.merge(summary_df, last_rpc_date_summary, on='CH Code', how='left')
    
    # Connected
    connected_mask = processed_df['Talk Time Duration'] > 0
    connected_counts = processed_df[connected_mask].groupby('CH Code').size().reset_index(name='Connected')
    summary_df = pd.merge(summary_df, connected_counts, on='CH Code', how='left')
    
    connected_records = processed_df[connected_mask].copy()
    if not connected_records.empty:
        latest_conn_idx = connected_records.groupby('CH Code')['Date'].idxmax()
        latest_conn_records = connected_records.loc[latest_conn_idx].copy()
        latest_conn_records['Formatted_Date'] = latest_conn_records['Date'].dt.strftime('%m%d%y').fillna('')
        latest_conn_records['Conn Status'] = latest_conn_records['Status'] + ' - ' + latest_conn_records['Formatted_Date']
        conn_status_summary = latest_conn_records[['CH Code', 'Conn Status']].copy()
        summary_df = pd.merge(summary_df, conn_status_summary, on='CH Code', how='left')
    else:
        empty_conn_status_df = pd.DataFrame({'CH Code': ch_codes, 'Conn Status': np.nan})
        summary_df = pd.merge(summary_df, empty_conn_status_df, on='CH Code', how='left')
    
    # Other status counts
    status_map = {
        'PTP FF': PTP_FF_STATUSES, 'SMS': SMS_STATUSES, 'EMAIL': EMAIL_STATUSES,
        'Pos Viber': POS_VIBER_STATUSES, 'Neg Viber': NEG_VIBER_STATUSES,
        'SOCMED LS': SOCMED_LS_STATUSES, 'POS FIELD': POS_FIELD_STATUSES,
        'NEG FIELD': NEG_FIELD_STATUSES, 'CONNECTED 3RD PARTY': CONNECTED_3RD_PARTY_STATUSES,
        'POS SKIP': POS_SKIP_STATUSES, 'NEG SKIP': NEG_SKIP_STATUSES
    }
    
    for col_name, status_list in status_map.items():
        counts = calculate_status_metric(processed_df, status_list)
        summary_df = pd.merge(summary_df, counts.rename(columns={'Result': col_name}), on='CH Code', how='left')
    
    # CALL, Broadcast, PM, PU
    cond1 = (processed_df['Remark Type'] == 'Follow Up') & (processed_df['Remark'].str.contains('Predictive', case=False, na=False))
    cond2 = (processed_df['Remark Type'] == 'Predictive') | (processed_df['Remark Type'] == 'Outgoing')
    call_mask = cond1 | cond2
    call_counts = processed_df[call_mask].groupby('CH Code').size().reset_index(name='CALL')
    summary_df = pd.merge(summary_df, call_counts, on='CH Code', how='left')
    
    broadcast_mask = processed_df['Remark'].str.contains('Broadcast', case=False, na=False)
    pm_mask_raw = broadcast_mask & processed_df['Status'].str.contains('PM', case=False, na=False)
    pu_mask_raw = broadcast_mask & processed_df['Status'].str.contains('PU', case=False, na=False)
    
    broadcast_counts = processed_df[broadcast_mask].groupby('CH Code').size().reset_index(name='Broadcast')
    pm_counts = processed_df[pm_mask_raw].groupby('CH Code').size().reset_index(name='PM')
    pu_counts = processed_df[pu_mask_raw].groupby('CH Code').size().reset_index(name='PU')
    
    summary_df = pd.merge(summary_df, broadcast_counts, on='CH Code', how='left')
    summary_df = pd.merge(summary_df, pm_counts, on='CH Code', how='left')
    summary_df = pd.merge(summary_df, pu_counts, on='CH Code', how='left')
    
    # Final formatting
    count_columns = list(status_map.keys()) + ['CONFIRMED', 'PTP', 'RPC', 'CALL', 'Broadcast', 'PM', 'PU', 'Connected']
    summary_df[count_columns] = summary_df[count_columns].fillna(0).astype(int)
    currency_columns = ['BALANCE', 'CONFIRMED ₱', 'PTP ₱']
    summary_df[currency_columns] = summary_df[currency_columns].fillna(0).round(2)
    summary_df = summary_df.sort_values(by='BALANCE', ascending=False).reset_index(drop=True)
    
    # UPDATED COLUMN ORDER: Remark after Cycle
    new_column_order = [
        'CH Code', 'Assign Date', 'Cycle', 'Remark', 'BALANCE', 
        'CONFIRMED', 'Last Confirmed Date', 'CONFIRMED ₱',
        'PTP', 'PTP ₱', 'Latest PTP Date', 'PTP FF', 'RPC', 'Last RPC Date',
        'Connected', 'Conn Status',
        'CALL', 'Broadcast', 'PM', 'PU', 'SMS', 'EMAIL',
        'Pos Viber', 'Neg Viber',
        'SOCMED LS', 'POS FIELD', 'NEG FIELD', 'CONNECTED 3RD PARTY',
        'POS SKIP', 'NEG SKIP'
    ]
    summary_df = summary_df.reindex(columns=new_column_order)
    summary_df[['Assign Date', 'Cycle', 'Remark', 'Latest PTP Date', 'Last RPC Date', 'Conn Status', 'Last Confirmed Date']] = \
        summary_df[['Assign Date', 'Cycle', 'Remark', 'Latest PTP Date', 'Last RPC Date', 'Conn Status', 'Last Confirmed Date']].fillna('')
    
    # --- Summary 4 ---
    summary_4_codes = summary_df[(summary_df['PM'] > 0) | (summary_df['PU'] > 0)]['CH Code'].unique()
    df4 = processed_df[processed_df['CH Code'].isin(summary_4_codes)].copy()
    summary_4_df = None
    if not df4.empty:
        pm_pu_mask_raw_all = (processed_df['Remark'].str.contains('Broadcast', case=False, na=False)) & \
                             (processed_df['Status'].str.contains('PM|PU', case=False, na=False))
        pm_pu_records_all = processed_df[pm_pu_mask_raw_all].copy()
        latest_pm_pu_date = pm_pu_records_all.groupby('CH Code')['Date'].max().reset_index(name='Latest PM/PU Date')
        df4 = pd.merge(df4, latest_pm_pu_date, on='CH Code', how='left')
        df4['Latest PM/PU Date'] = df4['Latest PM/PU Date'].fillna(pd.NaT)
        
        ptp_status_mask = df4['Status'].isin(PTP_STATUSES)
        ptp_date_greater_mask = (df4['Date'] > df4['Latest PM/PU Date'])
        conditional_ptp_mask = ptp_status_mask & ptp_date_greater_mask
        ptp_4_counts = df4[conditional_ptp_mask].groupby('CH Code').size().reset_index(name='PTP')
        
        confirmed_status_mask = df4['Status'].isin(CONFIRMED_STATUSES)
        confirmed_date_greater_mask = (df4['Date'] > df4['Claim Paid Date'])
        conditional_confirmed_mask = confirmed_status_mask & confirmed_date_greater_mask
        confirmed_4_counts = df4[conditional_confirmed_mask].groupby('CH Code').size().reset_index(name='CONFIRMED')
        
        rpc_status_mask = df4['Status'].isin(RPC_STATUSES)
        rpc_4_counts = df4[rpc_status_mask].groupby('CH Code').size().reset_index(name='RPC')
        
        context_cols = ['CH Code', 'Assign Date', 'Cycle', 'Remark', 'PTP ₱', 'CONFIRMED ₱', 'PM', 'PU']
        context_df = summary_df[summary_df['CH Code'].isin(summary_4_codes)][context_cols].copy()
        
        summary_4_df = pd.merge(context_df, ptp_4_counts, on='CH Code', how='left').fillna(0)
        summary_4_df = pd.merge(summary_4_df, confirmed_4_counts, on='CH Code', how='left').fillna(0)
        summary_4_df = pd.merge(summary_4_df, rpc_4_counts, on='CH Code', how='left').fillna(0)
        
        s4_column_order = [
            'CH Code', 'Assign Date', 'Cycle', 'Remark', 'PTP ₱', 'CONFIRMED ₱',
            'PM', 'PU', 'RPC', 'PTP', 'CONFIRMED'
        ]
        summary_4_df = summary_4_df.reindex(columns=s4_column_order)
        count_cols_s4 = ['PM', 'PU', 'RPC', 'PTP', 'CONFIRMED']
        currency_cols_s4 = ['PTP ₱', 'CONFIRMED ₱']
        summary_4_df[count_cols_s4] = summary_4_df[count_cols_s4].astype(int)
        summary_4_df[currency_cols_s4] = summary_4_df[currency_cols_s4].round(2)
        summary_4_df[['Assign Date', 'Cycle', 'Remark']] = summary_4_df[['Assign Date', 'Cycle', 'Remark']].fillna('')
    
    return summary_df, processed_df, summary_4_df

# --- 5. Streamlit Application Layout ---
st.set_page_config(layout="wide", page_title="Excel Data Aggregator & Filter")
st.title("📊 Multiple Excel File Summarizer")
st.markdown("Use the **sidebar** to upload your main data files and the optional filter file.")

with st.sidebar:
    st.header("📚 Main Data Files")
    uploaded_files = st.file_uploader(
        "Upload multiple main data Excel files (.xlsx)",
        type=['xlsx'],
        accept_multiple_files=True,
        key='main_uploader'
    )
    
    st.markdown("---")
    
    st.header("⚙️ CH Code Filter (Provides CH Code, Assign Date, Cycle, Remark)")
    filter_file = st.file_uploader(
        "Upload Filter File (Single XLSX) - Must have 'Old IC', 'Assign Date', 'Cycle' (Remark optional)",
        type=['xlsx'],
        accept_multiple_files=False,
        key='filter_uploader'
    )

ic_filter_set = None
merge_df = None
if filter_file:
    ic_filter_set, merge_df = extract_filter_ics(filter_file)
    if ic_filter_set:
        st.sidebar.success(f"Filter loaded: **{len(ic_filter_set)}** unique CH Codes.")
    elif merge_df is None:
        st.sidebar.error("Filter file missing required columns or could not be read.")

if uploaded_files:
    with st.spinner("Analyzing and calculating summaries..."):
        summary_df, processed_df, summary_4_df = process_data(uploaded_files, ic_filter_set, merge_df)
    
    if summary_df is not None:
        st.success("Summary generation complete!")
        
        currency_config = {
            "BALANCE": st.column_config.NumberColumn("BALANCE", format="₱%,.2f"),
            "CONFIRMED ₱": st.column_config.NumberColumn("CONFIRMED ₱", format="₱%,.2f"),
            "PTP ₱": st.column_config.NumberColumn("PTP ₱", format="₱%,.2f")
        }
        
        st.subheader("1️⃣ Full Summary Table by CH Code (Sorted by BALANCE)")
        st.dataframe(summary_df, hide_index=True, column_config=currency_config)
        
        csv_export_1 = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Full Summary (1) as CSV", data=csv_export_1, file_name='summary_1_full_results.csv', mime='text/csv')
        
        st.markdown("---")
        action_mask = (
            (summary_df['PTP'] > 0) | (summary_df['RPC'] > 0) |
            (summary_df['POS SKIP'] > 0) | (summary_df['POS FIELD'] > 0) |
            (summary_df['Pos Viber'] > 0)
        )
        no_conf_mask = (summary_df['CONFIRMED'] == 0)
        summary_2_df = summary_df[action_mask & no_conf_mask].copy()
        
        st.subheader("2️⃣ Action Taken, No Confirmation (Leads for Follow-up)")
        if summary_2_df.empty:
            st.info("No records with action but no confirmation.")
        else:
            st.info(f"Showing **{len(summary_2_df)}** actionable leads.")
            st.dataframe(summary_2_df, hide_index=True, column_config=currency_config)
            csv_export_2 = summary_2_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Actionable Leads (2) as CSV", data=csv_export_2, file_name='summary_2_actionable_leads.csv', mime='text/csv')
        
        st.markdown("---")
        ch_code_count = summary_df['CH Code'].nunique()
        aggregate_cols = [col for col in summary_df.columns if col not in ['CH Code', 'Assign Date', 'Cycle', 'Remark', 'Latest PTP Date', 'Last RPC Date', 'Conn Status', 'Last Confirmed Date']]
        summary_3_data = summary_df[aggregate_cols].sum().to_dict()
        summary_3_data = {'CH Code Count': ch_code_count, **summary_3_data}
        summary_3_df = pd.DataFrame(summary_3_data, index=['Total'])
        
        for col in ['BALANCE', 'CONFIRMED ₱', 'PTP ₱']:
            if col in summary_3_df.columns:
                summary_3_df[col] = summary_3_df[col].round(2)
        
        st.subheader("3️⃣ Aggregate Totals")
        display_cols = [
            'CH Code Count', 'BALANCE', 'CONFIRMED', 'CONFIRMED ₱', 'PTP', 'PTP ₱',
            'PTP FF', 'RPC', 'Connected', 'CALL', 'Broadcast', 'PM', 'PU',
            'SMS', 'EMAIL', 'Pos Viber', 'Neg Viber', 'SOCMED LS',
            'POS FIELD', 'NEG FIELD', 'CONNECTED 3RD PARTY', 'POS SKIP', 'NEG SKIP'
        ]
        st.dataframe(summary_3_df[display_cols], hide_index=False, column_config={
            "CH Code Count": st.column_config.NumberColumn("CH Code Count", format="%d"),
            "BALANCE": st.column_config.NumberColumn("TOTAL BALANCE", format="₱%,.2f"),
            "CONFIRMED ₱": st.column_config.NumberColumn("TOTAL CONFIRMED ₱", format="₱%,.2f"),
            "PTP ₱": st.column_config.NumberColumn("TOTAL LATEST PTP ₱", format="₱%,.2f")
        })
        
        csv_export_3 = summary_3_df.to_csv().encode('utf-8')
        st.download_button("Download Aggregate Summary (3) as CSV", data=csv_export_3, file_name='summary_3_aggregate_totals.csv', mime='text/csv')
        
        st.markdown("---")
        st.subheader("4️⃣ Unique CH Code Count (PM/PU Leads)")
        if summary_4_df is None:
            st.info("No CH Codes with PM or PU activity.")
        else:
            ch_code_count_s4 = summary_4_df['CH Code'].nunique()
            st.metric("Total Unique CH Codes with PM or PU", value=ch_code_count_s4)
            st.caption("Detailed breakdown available for download.")
            csv_export_4 = summary_4_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Detailed PM/PU Summary (4) as CSV", data=csv_export_4, file_name='summary_4_pm_pu_detailed.csv', mime='text/csv')
        
        st.markdown("---")
        with st.expander("View Filtered Raw Data"):
            st.write(f"Total rows: **{len(processed_df)}**")
            st.dataframe(processed_df)