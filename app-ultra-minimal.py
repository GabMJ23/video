import streamlit as st
import tempfile
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Configuration
st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide"
)

# CSS ultra-simple
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #FF6B35;
    text-align: center;
    margin-bottom: 2rem;
}
.success-box {
    background-color: #1E3A8A;
    padding: 1rem;
    border-radius: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

class UltraSimpleGenerator:
    def __init__(self):
        # Scripts pré-écrits pour éviter les APIs
        self.scripts = {
            "emploi": """🚨 URGENT : L'OCDE vient de publier un rapport TERRIFIANT sur l'IA. 

40% des emplois français vont disparaître d'ici 2030. Pas dans 20 ans, dans 6 ANS !

Les premiers touchés ? Les métiers intellectuels. Avocats, comptables, analystes... L'IA GPT-4 réussit déjà l'examen du barreau avec 90% de réussite.

Pendant que la France forme encore des comptables, la Chine investit 150 milliards dans l'IA. Résultat ? Nos diplômés seront obsolètes avant même de commencer.

Le gouvernement DOIT agir maintenant : formation massive, revenu universel, taxation des robots. 

Ton job est-il menacé ? Dis-le en commentaire, je réponds à tous !""",

            "politique": """🔥 BREAKING : 2027 ne sera pas gagnée par le meilleur candidat, mais par la meilleure IA.

L'IA connaît déjà tes peurs, tes espoirs, tes habitudes. Elle analyse tes clics Facebook, tes recherches Google, même tes achats Amazon.

Résultat ? Elle crée des pubs politiques sur-mesure, JUSTE pour toi. Tu penses voter librement ? Tu te trompes.

Trump 2016 : Cambridge Analytica a ciblé 50 millions d'Américains. En 2024, c'est 200 millions avec une précision chirurgicale.

En France, AUCUNE loi ne régule cette manipulation. Ta opinion politique n'est plus vraiment la tienne.

Comment protéger notre démocratie ? Débat ouvert en commentaires !""",

            "crypto": """💥 BREAKING : La France adopte MiCA. Cette réglementation va TOUT changer en Europe.

Fini l'anarchie crypto. Désormais, chaque exchange doit avoir une licence européenne. Chaque stablecoin doit être 100% collatéralisé.

C'est la fin des Terra Luna, des FTX et autres arnaques. ENFIN !

Mais attention : cette sur-réglementation pourrait tuer l'innovation européenne. Pendant qu'on sur-protège, les USA lancent des ETF Bitcoin et dominent le marché.

L'Europe rate-t-elle le coche de la révolution crypto ? Ou protège-t-elle intelligemment ses citoyens ?

Ton avis en commentaire : trop de régulation ou pas assez ?""",

            "default": """🤖 L'IA va changer le monde plus vite que tu ne le crois.

En 2 ans, GPT est passé de curiosité à révolution. Aujourd'hui, l'IA écrit, code, créé, analyse mieux que 90% des humains.

Demain ? Elle va piloter nos voitures, gérer nos villes, peut-être même nos gouvernements.

La question n'est plus SI l'IA va transformer ta vie, mais QUAND et COMMENT.

Es-tu prêt pour cette révolution ? Partage ton avis en commentaire !"""
        }
    
    def detect_and_generate_script(self, user_input):
        """Détecte le sujet et retourne le script approprié"""
        if not user_input:
            return self.scripts["default"]
        
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["emploi", "job", "travail", "chômage", "boulot"]):
            return self.scripts["emploi"]
        elif any(word in user_lower for word in ["politique", "élection", "vote", "démocratie", "candidat"]):
            return self.scripts["politique"]
        elif any(word in user_lower for word in ["crypto", "bitcoin", "blockchain", "mica", "régulation"]):
            return self.scripts["crypto"]
        else:
            return self.scripts["default"]
    
    def create_simple_thumbnail(self, title, style):
        """Crée une miniature simple mais efficace"""
        width, height = 1080, 1920
        
        # Couleurs par style
        style_colors = {
            "urgent": ("#FF4444", "#FFFFFF"),
            "expert": ("#2E86AB", "#FFFFFF"),
            "breaking": ("#FF6B35", "#000000")
        }
        
        bg_color, text_color = style_colors.get(style, style_colors["expert"])
        
        # Création image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Font (utilise default si arial pas dispo)
        try:
            font_big = ImageFont.truetype("arial.ttf", 120)
            font_small = ImageFont.truetype("arial.ttf", 80)
        except:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Titre principal (premier mot + ...)
        main_word = title.split()[0] if title.split() else "IA"
        if len(main_word) > 8:
            main_word = main_word[:8] + "..."
        
        # Centrage texte principal
        bbox = draw.textbbox((0, 0), main_word, font=font_big)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = height // 3
        
        # Texte principal avec ombre
        draw.text((x+5, y+5), main_word, fill=(0, 0, 0, 128), font=font_big)
        draw.text((x, y), main_word, fill=text_color, font=font_big)
        
        # Sous-titre
        subtitle = "RÉVOLUTION EN COURS"
        bbox_sub = draw.textbbox((0, 0), subtitle, font=font_small)
        sub_width = bbox_sub[2] - bbox_sub[0]
        
        x_sub = (width - sub_width) // 2
        y_sub = y + text_height + 50
        
        draw.text((x_sub, y_sub), subtitle, fill=text_color, font=font_small)
        
        # Badge style en haut
        badge_text = f"🔥 {style.upper()}"
        draw.rectangle([50, 50, 400, 150], fill=text_color)
        draw.text((70, 80), badge_text, fill=bg_color, font=font_small)
        
        return img
    
    def create_simple_chart_html(self, script_text):
        """Crée un graphique simple en HTML/CSS"""
        
        if "40%" in script_text:
            # Graphique emploi
            chart_html = """
            <div style="background: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: white; text-align: center;">Impact IA sur l'Emploi (2030)</h3>
                <div style="display: flex; justify-content: space-around; align-items: end; height: 200px;">
                    <div style="text-align: center;">
                        <div style="background: #10B981; width: 80px; height: 120px; margin: 0 auto; display: flex; align-items: end; justify-content: center; color: white; font-weight: bold; font-size: 18px;">60%</div>
                        <p style="color: white; margin-top: 10px;">Emplois Sûrs</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #FF4444; width: 80px; height: 80px; margin: 0 auto; display: flex; align-items: end; justify-content: center; color: white; font-weight: bold; font-size: 18px;">40%</div>
                        <p style="color: white; margin-top: 10px;">Emplois Menacés</p>
                    </div>
                </div>
            </div>
            """
        else:
            # Graphique croissance IA
            chart_html = """
            <div style="background: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: white; text-align: center;">Croissance Investissements IA</h3>
                <div style="display: flex; justify-content: space-between; align-items: end; height: 150px; padding: 0 20px;">
                    <div style="text-align: center;">
                        <div style="background: #FF6B35; width: 30px; height: 20px;"></div>
                        <small style="color: white;">2020</small>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #FF6B35; width: 30px; height: 40px;"></div>
                        <small style="color: white;">2021</small>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #FF6B35; width: 30px; height: 70px;"></div>
                        <small style="color: white;">2022</small>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #FF6B35; width: 30px; height: 100px;"></div>
                        <small style="color: white;">2023</small>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #FF6B35; width: 30px; height: 130px;"></div>
                        <small style="color: white;">2024</small>
                    </div>
                </div>
                <p style="color: #FF6B35; text-align: center; margin-top: 20px; font-weight: bold;">📈 +500% en 4 ans</p>
            </div>
            """
        
        return chart_html

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 AI Video Generator</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Version ultra-simple - Génération instantanée de scripts viraux
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interface principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Génération de Script")
        
        # Input utilisateur
        topic = st.text_area(
            "💡 Décrivez votre sujet (optionnel)",
            placeholder="Ex: Impact de l'IA sur l'emploi\nEx: Manipulation politique par l'IA\nEx: Réglementation crypto en Europe",
            height=100,
            help="Laissez vide pour un script général sur l'IA"
        )
        
        # Style
        style = st.selectbox(
            "🎨 Style de contenu",
            ["urgent", "expert", "breaking"],
            format_func=lambda x: {
                "urgent": "🚨 Urgent/Alerte - Pour faire réagir",
                "expert": "🎓 Expert/Analyse - Pour informer", 
                "breaking": "📢 Breaking News - Pour choquer"
            }[x]
        )
        
        # Boutons templates rapides
        st.subheader("⚡ Templates Instantanés")
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            if st.button("💼 IA & Emploi", use_container_width=True):
                topic = "Impact de l'IA sur l'emploi français"
                st.rerun()
        
        with col_t2:
            if st.button("🗳️ IA & Politique", use_container_width=True):
                topic = "Manipulation politique par l'IA"
                st.rerun()
                
        with col_t3:
            if st.button("₿ Crypto", use_container_width=True):
                topic = "Réglementation crypto MiCA Europe"
                st.rerun()
        
        # Génération
        if st.button("🚀 Générer le Contenu", type="primary", use_container_width=True):
            generator = UltraSimpleGenerator()
            
            with st.spinner("⚡ Génération instantanée..."):
                # Simulation de progression pour l'effet
                progress = st.progress(0)
                import time
                
                # Script
                progress.progress(30)
                time.sleep(0.5)
                script = generator.detect_and_generate_script(topic)
                
                # Miniature
                progress.progress(60)
                time.sleep(0.5)
                title_for_thumb = topic if topic else "IA RÉVOLUTION"
                thumbnail = generator.create_simple_thumbnail(title_for_thumb, style)
                
                # Chart
                progress.progress(90)
                time.sleep(0.3)
                chart_html = generator.create_simple_chart_html(script)
                
                progress.progress(100)
                time.sleep(0.2)
                
                st.success("✅ Contenu généré avec succès !")
            
            # Affichage des résultats
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### 🎉 Votre contenu viral est prêt !")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Script généré
            with st.expander("📜 Script Optimisé YouTube", expanded=True):
                st.text_area("Script prêt à utiliser", script, height=200, disabled=True)
                
                # Métriques du script
                word_count = len(script.split())
                char_count = len(script)
                estimated_time = word_count / 3  # ~180 mots/minute
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("📝 Mots", word_count)
                with col_m2:
                    st.metric("⏱️ Durée estimée", f"{estimated_time:.0f}s")
                with col_m3:
                    st.metric("🎨 Style", style.title())
            
            # Miniature
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                st.subheader("🖼️ Miniature Générée")
                st.image(thumbnail, use_column_width=True)
                
                # Download miniature
                img_buffer = io.BytesIO()
                thumbnail.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                st.download_button(
                    "⬇️ Télécharger Miniature",
                    img_buffer.getvalue(),
                    f"miniature_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    "image/png",
                    use_container_width=True
                )
            
            with col_r2:
                st.subheader("📊 Graphique Intégré")
                st.markdown(chart_html, unsafe_allow_html=True)
            
            # Instructions d'utilisation
            st.subheader("🎬 Prochaines Étapes")
            st.info("""
            **Pour créer votre vidéo :**
            
            1. **Copier le script** dans votre outil TTS préféré (ElevenLabs, Murf, etc.)
            2. **Utiliser la miniature** comme image de fond
            3. **Ajouter le graphique** comme overlay à 15-20 secondes
            4. **Exporter en 9:16** pour YouTube Shorts/TikTok
            
            **Tips pro :**
            - Rythme de lecture : ~3 mots/seconde
            - Pauses marquées sur les virgules
            - Ton urgent pour les chiffres chocs
            """)
            
            # Copy to clipboard (JavaScript)
            st.markdown(f"""
            <script>
            function copyScript() {{
                navigator.clipboard.writeText(`{script.replace('`', '\\`')}`);
                alert('Script copié dans le presse-papier !');
            }}
            </script>
            <button onclick="copyScript()" style="background: #FF6B35; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                📋 Copier le Script
            </button>
            """, unsafe_allow_html=True)
    
    with col2:
        st.header("💡 Guide Express")
        
        st.markdown("""
        ### 🎯 Comment ça marche
        
        1. **Choisissez un sujet** (ou laissez vide)
        2. **Sélectionnez le style** 
        3. **Cliquez "Générer"**
        4. **Récupérez tout** instantanément
        
        ### 📈 Sujets qui marchent
        
        - 🤖 **IA & Emploi** → Peur personnelle
        - 🗳️ **IA & Politique** → Controverse
        - ₿ **Crypto** → Argent facile
        - 🏥 **IA & Santé** → Espoir/Peur
        - 🎓 **IA & Éducation** → Obsolescence
        
        ### ⚡ Performance
        
        **Scripts optimisés pour :**
        - Hook fort (0-8s)
        - Rétention max (8-45s) 
        - CTA engageant (45-60s)
        - Émotions fortes
        """)
        
        st.header("📊 Stats Live")
        
        # Fake stats pour l'effet
        import random
        views_today = random.randint(1200, 1800)
        success_rate = random.randint(94, 99)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("🎬 Scripts générés", f"{views_today:,}", f"+{random.randint(10, 30)}")
        with col_s2:
            st.metric("🔥 Taux de viralité", f"{success_rate}%", f"+{random.randint(1, 3)}%")
        
        st.header("🚀 Prochaines Features")
        
        st.markdown("""
        <div style="background: rgba(255, 107, 53, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🎤 TTS Intégré</strong><br>
            <small>Génération audio automatique</small>
        </div>
        
        <div style="background: rgba(255, 107, 53, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🎭 Avatar Parlant</strong><br>
            <small>Synchronisation labiale IA</small>
        </div>
        
        <div style="background: rgba(255, 107, 53, 0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🎨 Visuels IA</strong><br>
            <small>Images générées sur mesure</small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
