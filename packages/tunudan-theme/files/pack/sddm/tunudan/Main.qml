// Écran de connexion SDDM Tunudan — compatible Qt 5 (SDDM 0.20) et Qt 6 (SDDM 0.21)
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#0D0D0D"

    readonly property color accent: config.accent ? config.accent : "#FF6B1A"
    readonly property color ink: "#F5F1EA"
    readonly property color muted: "#A39E96"
    readonly property color panel: "#E6141416"
    readonly property string fontName: config.font ? config.font : "Inter"
    property int sessionIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
    property string message: ""

    Image {
        anchors.fill: parent
        source: config.background ? config.background : "background.png"
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "#D90D0D0D" }
            GradientStop { position: 0.55; color: "#660D0D0D" }
            GradientStop { position: 1.0; color: "#000D0D0D" }
        }
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.message = "Mot de passe incorrect, réessayez."
            password.text = ""
            password.forceActiveFocus()
            shake.start()
        }
        function onLoginSucceeded() { root.message = "" }
    }

    // Horloge et date
    Column {
        anchors.left: parent.left
        anchors.leftMargin: root.width * 0.07
        anchors.top: parent.top
        anchors.topMargin: root.height * 0.11
        spacing: 4
        Text {
            id: clock
            font.family: root.fontName
            font.pixelSize: Math.round(root.height * 0.11)
            font.weight: Font.Bold
            color: root.ink
            text: Qt.formatTime(new Date(), config.timeFormat ? config.timeFormat : "HH:mm")
        }
        Text {
            id: date
            font.family: root.fontName
            font.pixelSize: Math.round(root.height * 0.028)
            color: root.accent
            text: new Date().toLocaleDateString(Qt.locale("fr_FR"), config.dateFormat ? config.dateFormat : "dddd d MMMM")
        }
        Timer {
            interval: 1000; running: true; repeat: true
            onTriggered: {
                clock.text = Qt.formatTime(new Date(), config.timeFormat ? config.timeFormat : "HH:mm")
                date.text = new Date().toLocaleDateString(Qt.locale("fr_FR"), config.dateFormat ? config.dateFormat : "dddd d MMMM")
            }
        }
    }

    // Carte de connexion
    Rectangle {
        id: card
        width: Math.min(460, root.width * 0.9)
        height: form.implicitHeight + 64
        anchors.left: parent.left
        anchors.leftMargin: root.width * 0.07
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: root.height * 0.08
        radius: 18
        color: root.panel
        border.color: "#2A2A2C"
        border.width: 1

        // liseré orange en haut, comme un pli
        Rectangle { width: parent.width - 36; height: 3; radius: 2; color: root.accent; anchors.top: parent.top; anchors.horizontalCenter: parent.horizontalCenter }

        SequentialAnimation {
            id: shake
            NumberAnimation { target: card; property: "anchors.leftMargin"; to: root.width * 0.07 + 12; duration: 50 }
            NumberAnimation { target: card; property: "anchors.leftMargin"; to: root.width * 0.07 - 12; duration: 70 }
            NumberAnimation { target: card; property: "anchors.leftMargin"; to: root.width * 0.07; duration: 50 }
        }

        ColumnLayout {
            id: form
            anchors.fill: parent
            anchors.margins: 32
            spacing: 14

            RowLayout {
                spacing: 14
                Image { source: "logo.svg"; sourceSize.width: 54; sourceSize.height: 54; Layout.preferredWidth: 54; Layout.preferredHeight: 54 }
                Column {
                    Text { text: "Tunudan OS"; color: root.ink; font.family: root.fontName; font.pixelSize: 26; font.weight: Font.Bold }
                    Text { text: "Apprendre. Coder. Avancer."; color: root.muted; font.family: root.fontName; font.pixelSize: 14 }
                }
            }

            Item { Layout.preferredHeight: 4 }

            Text { text: "Utilisateur"; color: root.muted; font.family: root.fontName; font.pixelSize: 13 }
            ComboBox {
                id: user
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                model: userModel
                textRole: "name"
                currentIndex: userModel.lastIndex >= 0 ? userModel.lastIndex : 0
                font.family: root.fontName
                font.pixelSize: 17
                background: Rectangle { radius: 10; color: "#1C1C1E"; border.color: user.activeFocus ? root.accent : "#3A3A3E"; border.width: user.activeFocus ? 2 : 1 }
                contentItem: Text {
                    leftPadding: 14
                    verticalAlignment: Text.AlignVCenter
                    text: user.displayText
                    color: root.ink
                    font: user.font
                }
                delegate: ItemDelegate {
                    width: user.width
                    contentItem: Text { text: model.realName ? model.realName + "  (" + model.name + ")" : model.name; color: highlighted ? "#0D0D0D" : root.ink; font.family: root.fontName; font.pixelSize: 16 }
                    highlighted: user.highlightedIndex === index
                    background: Rectangle { color: highlighted ? root.accent : "#1C1C1E" }
                }
                popup.background: Rectangle { color: "#1C1C1E"; border.color: "#3A3A3E"; radius: 8 }
            }

            Text { text: "Mot de passe"; color: root.muted; font.family: root.fontName; font.pixelSize: 13 }
            TextField {
                id: password
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                echoMode: TextInput.Password
                placeholderText: "••••••••"
                placeholderTextColor: "#5A5753"
                color: root.ink
                font.family: root.fontName
                font.pixelSize: 17
                leftPadding: 14
                focus: true
                background: Rectangle { radius: 10; color: "#1C1C1E"; border.color: password.activeFocus ? root.accent : "#3A3A3E"; border.width: password.activeFocus ? 2 : 1 }
                Keys.onReturnPressed: root.doLogin()
                Keys.onEnterPressed: root.doLogin()
            }

            Text {
                text: root.message
                visible: root.message !== ""
                color: "#FF7A5C"
                font.family: root.fontName
                font.pixelSize: 14
            }

            Button {
                id: loginButton
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                text: "Se connecter"
                font.family: root.fontName
                font.pixelSize: 17
                font.weight: Font.Bold
                onClicked: root.doLogin()
                contentItem: Text { text: loginButton.text; font: loginButton.font; color: "#0D0D0D"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                background: Rectangle { radius: 12; color: loginButton.down ? "#C2410C" : (loginButton.hovered ? "#FF9A5C" : root.accent) }
            }

            RowLayout {
                Layout.fillWidth: true
                Text { text: "Bureau"; color: root.muted; font.family: root.fontName; font.pixelSize: 13 }
                ComboBox {
                    id: session
                    Layout.fillWidth: true
                    model: sessionModel
                    textRole: "name"
                    currentIndex: root.sessionIndex
                    onActivated: root.sessionIndex = currentIndex
                    font.family: root.fontName
                    font.pixelSize: 14
                    background: Rectangle { radius: 8; color: "transparent"; border.color: "#3A3A3E" }
                    contentItem: Text { leftPadding: 10; verticalAlignment: Text.AlignVCenter; text: session.displayText; color: root.ink; font: session.font; elide: Text.ElideRight }
                    delegate: ItemDelegate {
                        width: session.width
                        contentItem: Text { text: model.name; color: highlighted ? "#0D0D0D" : root.ink; font.family: root.fontName; font.pixelSize: 14 }
                        highlighted: session.highlightedIndex === index
                        background: Rectangle { color: highlighted ? root.accent : "#1C1C1E" }
                    }
                    popup.background: Rectangle { color: "#1C1C1E"; border.color: "#3A3A3E"; radius: 8 }
                }
            }
        }
    }

    // Boutons d'alimentation
    Row {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 32
        spacing: 12
        Repeater {
            model: [
                { label: "Veille", action: "suspend", enabled: sddm.canSuspend },
                { label: "Redémarrer", action: "reboot", enabled: sddm.canReboot },
                { label: "Éteindre", action: "poweroff", enabled: sddm.canPowerOff }
            ]
            delegate: Button {
                id: pb
                visible: modelData.enabled
                text: modelData.label
                font.family: root.fontName
                font.pixelSize: 14
                onClicked: {
                    if (modelData.action === "suspend") sddm.suspend()
                    else if (modelData.action === "reboot") sddm.reboot()
                    else sddm.powerOff()
                }
                contentItem: Text { text: pb.text; font: pb.font; color: root.ink; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                background: Rectangle { implicitWidth: 120; implicitHeight: 40; radius: 10; color: pb.hovered ? "#3A3A3E" : "#B31C1C1E"; border.color: "#3A3A3E" }
            }
        }
    }

    Text {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.margins: 32
        text: sddm.hostName + "  ·  tunudan.fr"
        color: root.muted
        font.family: root.fontName
        font.pixelSize: 13
    }

    function doLogin() {
        root.message = ""
        sddm.login(user.currentText, password.text, root.sessionIndex)
    }

    Component.onCompleted: password.forceActiveFocus()
}
