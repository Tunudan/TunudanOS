/* Diaporama d'installation Tunudan OS (5 écrans) */
import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation {
    id: presentation

    function nextSlide() { presentation.goToNextSlide(); }

    Timer {
        id: advanceTimer
        interval: 7000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: nextSlide()
    }

    component TSlide: Slide {
        property string titre: ""
        property string texte: ""
        Rectangle { anchors.fill: parent; color: "#0D0D0D" }
        Image {
            id: logo
            source: "logo.png"
            width: 96; height: 96
            fillMode: Image.PreserveAspectFit
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top; anchors.topMargin: 40
        }
        Text {
            id: t
            text: titre
            color: "#FF6B1A"
            font.pixelSize: 30; font.bold: true; font.family: "Inter"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: logo.bottom; anchors.topMargin: 24
        }
        Text {
            text: texte
            color: "#F5F1EA"
            font.pixelSize: 18; font.family: "Inter"
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            width: parent.width * 0.75
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: t.bottom; anchors.topMargin: 18
        }
    }

    TSlide { titre: "Bienvenue dans Tunudan OS"; texte: "Un Linux simple, sûr et prêt à l'emploi. Apprendre. Coder. Avancer." }
    TSlide { titre: "Toujours à jour"; texte: "Les mises à jour de sécurité s'installent toutes seules. Vous n'avez rien à faire." }
    TSlide { titre: "Une aide à portée de clic"; texte: "Le bouton « Appeler Tunudan » permet à un formateur de vous aider à distance, en toute sécurité." }
    TSlide { titre: "Des cours en visio"; texte: "Linux, cybersécurité, développement, IA : les cours Tunudan utilisent ce système. Rendez-vous sur tunudan.fr." }
    TSlide { titre: "Presque fini"; texte: "L'installation se termine. Au redémarrage, l'assistant d'accueil vous guidera." }

    function onActivate() { presentation.currentSlide = 0; }
    function onLeave() { }
}
