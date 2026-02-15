# Phishing Detection System - Test URLs

## ✅ SAFE URLs (Legitimate Websites)

These URLs should be classified as **SAFE** with high confidence:

1. `https://google.com` - Expected: SAFE (~99%)
2. `https://github.com` - Expected: SAFE (~99%)
3. `https://microsoft.com` - Expected: SAFE (~99%)
4. `https://amazon.com` - Expected: SAFE (~99%)
5. `https://facebook.com` - Expected: SAFE (~99%)
6. `https://twitter.com` - Expected: SAFE (~99%)
7. `https://netflix.com` - Expected: SAFE (~99%)
8. `https://apple.com` - Expected: SAFE (~99%)
9. `https://stackoverflow.com` - Expected: SAFE (~99%)
10. `https://python.org` - Expected: SAFE (~99%)

## 🚨 PHISHING URLs (Malicious/Suspicious)

These URLs should be classified as **PHISHING DETECTED** with high confidence:

### IP-Based Phishing (Very High Risk)
11. `http://192.168.1.1/paypal-verify-account.com` - Expected: PHISHING (100%)
12. `http://10.0.0.1/bank-login-secure.com` - Expected: PHISHING (100%)
13. `http://172.16.0.1/microsoft-account-verify.com` - Expected: PHISHING (100%)

### Suspicious TLD + Keywords
14. `https://secure-account-verify-login-update.tk` - Expected: PHISHING (90-95%)
15. `https://paypal-security-verify.tk` - Expected: PHISHING (90-95%)
16. `https://facebook-account-recovery-verify.ml` - Expected: PHISHING (90-95%)

### Long URLs with Suspicious Patterns
17. `https://microsoft-account-security-verification-update.com` - Expected: PHISHING (85-95%)
18. `https://amazon-payment-method-update-required.com` - Expected: PHISHING (85-95%)
19. `https://apple-id-security-verification-required.com` - Expected: PHISHING (85-95%)

### URLs with @ Symbol (Redirect Trick)
20. `https://google.com@malicious-site.com` - Expected: PHISHING (95-100%)
21. `https://paypal.com@phishing-site.tk` - Expected: PHISHING (95-100%)

### Multiple Subdomains
22. `https://login.secure.verify.account.paypal-update.com` - Expected: PHISHING (80-90%)
23. `https://www.secure.login.microsoft.account-verify.com` - Expected: PHISHING (80-90%)

## 🔍 Model Features Analyzed

For each URL, the model analyzes:

1. **url_length** - Total character count (longer = more suspicious)
2. **has_ip** - Contains IP address instead of domain (major red flag)
3. **has_at_symbol** - Contains @ symbol (redirect trick)
4. **has_dash** - Contains dashes in domain (common in phishing)
5. **is_https** - Uses HTTPS protocol (safer, but not guarantee)
6. **subdomain_count** - Number of subdomains (many = suspicious)

## 📊 Model Performance

- **Accuracy**: 96.43% (5-fold cross-validation)
- **Training Samples**: 420 URLs (210 safe, 210 phishing)
- **Algorithm**: Random Forest Classifier (100 trees)
- **Most Important Features**:
  1. URL Length (44.39%)
  2. Subdomain Count (27.94%)
  3. Has IP Address (8.99%)

## 🎯 How to Test

1. Open your browser and go to: `http://127.0.0.1:5001`
2. Enter any URL from the lists above
3. Click "Analyze URL"
4. Check the result matches the expected classification
5. View the confidence score and extracted features

## 💡 Tips for Testing

- **Safe URLs**: Try well-known legitimate websites
- **Phishing URLs**: Look for URLs with:
  - IP addresses instead of domains
  - Suspicious keywords (verify, secure, account, login, update)
  - Unusual TLDs (.tk, .ml, .ga, .cf)
  - Multiple dashes or subdomains
  - @ symbols in the URL
  - Very long URLs

## ⚠️ Important Notes

- This is a **demonstration model** for educational purposes
- Real phishing detection requires more sophisticated analysis
- Always verify URLs through official channels
- Never enter credentials on suspicious websites
- The model analyzes URL structure, not actual website content
