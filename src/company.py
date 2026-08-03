import streamlit as st


def display_company_profile(info):

    with st.container(border=True):

        st.subheader("🏢 Company Overview")

        company_name = info.get("longName", "Unknown Company")
        symbol = info.get("symbol", "")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        country = info.get("country", "N/A")
        employees = info.get("fullTimeEmployees")
        website = info.get("website", "")
        summary = info.get("longBusinessSummary", "No description available.")

        st.markdown(f"### {company_name}")

        if symbol:
         st.caption(f"Ticker: {symbol}")

        st.write(f"**Sector:** {sector}")
        st.write(f"**Industry:** {industry}")

        if employees:
            st.write(f"**Employees:** {employees:,}")
        else:
            st.write("**Employees:** N/A")

        st.write(f"**Country:** {country}")

        if website:
            st.markdown(f"🌐 **Website:** {website}")

    with st.expander("📖 About Company"):

     st.write(summary)       